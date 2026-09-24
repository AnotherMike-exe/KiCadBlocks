"""Acceptance test after Update PCB from Schematic on a module board.

Usage: check_import.py <Modules/Block directory>

Checks, and exits 1 if any fails:
  1. Every schematic symbol that goes on the board has one footprint, same references.
  2. Every net class pattern in the .kicad_pro binds to at least one board net.
  3. The .kicad_dru loaded: a copy with a 3 mm clearance rule appended must
     raise the DRC violation count (the canary).
"""
import json, os, re, shutil, subprocess, sys, tempfile
from fnmatch import fnmatchcase

CLI = "/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli"


def sch_refs(text):
    refs = set()
    for m in re.finditer(r'\n\s*\(symbol\s*\(lib_id "([^"]+)"([\s\S]*?)\n\s*\(instances', text):
        body = m.group(2)
        if re.search(r'\(on_board no\)', body) or m.group(1).startswith("power:"):
            continue
        r = re.search(r'\(property "Reference" "([^"]+)"', body)
        if r and not r.group(1).startswith("#"):
            refs.add(r.group(1))
    return refs


def pcb_refs(text):
    return set(re.findall(r'\(property "Reference" "([^"]+)"', text)) - {"REF**"}


def pcb_nets(text):
    # KiCad 10 names the net on each item, (net "name"). KiCad 9 used (net N "name").
    return set(re.findall(r'\(net (?:\d+ )?"([^"]*)"\)', text)) - {""}


def drc_count(board):
    out = os.path.join(os.path.dirname(board), "drc.json")
    subprocess.run([CLI, "pcb", "drc", "--format", "json", "--severity-all",
                    "--refill-zones", "-o", out, board], capture_output=True)
    return len(json.load(open(out))["violations"])


def main(d):
    d = d.rstrip("/"); name = os.path.basename(d); ok = True
    sch = open(f"{d}/{name}.kicad_sch").read(); pcb = open(f"{d}/{name}.kicad_pcb").read()
    s, p = sch_refs(sch), pcb_refs(pcb)
    print(f"{name}: {len(s)} symbols, {len(p)} footprints")
    if s != p:
        ok = False; print("  FAIL refs  missing on board:", sorted(s - p), " extra:", sorted(p - s))
    nets = pcb_nets(pcb)
    for pat in json.load(open(f"{d}/{name}.kicad_pro"))["net_settings"]["netclass_patterns"]:
        hit = [n for n in nets if fnmatchcase(n, pat["pattern"])]
        if not hit:
            ok = False; print(f"  FAIL class {pat['netclass']}: pattern {pat['pattern']} binds to nothing")
    with tempfile.TemporaryDirectory() as t:
        for f in os.listdir(d):
            if f.startswith(name + ".kicad_") or f.endswith("lib-table"):
                shutil.copy(f"{d}/{f}", t)
        base = drc_count(f"{t}/{name}.kicad_pcb")
        with open(f"{t}/{name}.kicad_dru", "a") as f:
            f.write('\n(rule "canary"\n(constraint clearance (min 3mm))\n(condition "A.Net != B.Net"))\n')
        canary = drc_count(f"{t}/{name}.kicad_pcb")
    print(f"  drc {base} -> canary {canary}")
    if canary <= base:
        ok = False; print("  FAIL canary: the .kicad_dru did not load")
    print("  PASS" if ok else "  FAILED")
    return ok


if __name__ == "__main__":
    sys.exit(0 if all([main(a) for a in sys.argv[1:]]) else 1)
