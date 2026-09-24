#!/usr/bin/env python3
"""List or delete zones in a KiCad 10 board file.

Konnect has no zone delete and no zone edit. `add_copper_pour` only appends.
This fills the gap so a zone can be replaced rather than duplicated.

SAFE ONLY WHEN a zone's uuid appears exactly once in the file. A zone carries
no cross-reference, and nothing else points at it, so removing the whole
balanced `(zone ...)` block leaves the rest untouched. The script REFUSES to
delete a uuid it finds more than once, which is what a group membership looks
like. Checked on this board 2026-09-23: 0 groups, 6 zones, 1 occurrence each.

CLOSE THE BOARD IN pcbnew FIRST. This writes the file. pcbnew holds its own
copy in memory, and its next save overwrites whatever this wrote.

Usage:
  python3 zone_tool.py list   <board.kicad_pcb>
  python3 zone_tool.py delete <board.kicad_pcb> <uuid> [<uuid> ...]
"""
import re, sys, shutil, os, datetime

def blocks(src, tag):
    """Yield (start, end) of each balanced s-expression starting with tag."""
    i = 0
    while True:
        i = src.find(tag, i)
        if i < 0:
            return
        j = i + 1
        depth = 0
        while True:
            c = src[j]
            if c == '"':
                j += 1
                while src[j] != '"' or src[j-1] == '\\':
                    j += 1
            elif c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        yield (i, j + 1)
        i = j

def paren_balance(s):
    d = 0; instr = False; i = 0
    while i < len(s):
        c = s[i]
        if instr:
            if c == '\\':
                i += 2; continue
            if c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c == '(':
                d += 1
            elif c == ')':
                d -= 1
        i += 1
    return d

def zones(s):
    out = []
    spans = list(blocks(s, '\n\t(zone')) + list(blocks(s, '\n  (zone'))
    # pcbnew writes a zone with a tab indent. Konnect `add_copper_pour` appends
    # one with two spaces. Scan for both, or an appended zone stays invisible.
    # Measured 2026-09-23.
    for a, b in sorted(spans):
        zb = s[a:b]
        u = re.search(r'\(uuid "([^"]+)"\)', zb)
        net = re.search(r'\(net "([^"]*)"\)', zb) or re.search(r'\(net_name "([^"]*)"\)', zb)
        lay = re.search(r'\(layers?\s+"([^"]+)"', zb)
        k = zb.find('(polygon'); fp = zb.find('(filled_polygon')
        pts = re.findall(r'\(xy ([-\d.]+) ([-\d.]+)\)', zb[k:fp if fp > 0 else len(zb)])
        xs = [float(p[0]) for p in pts]; ys = [float(p[1]) for p in pts]
        out.append({'a': a, 'b': b, 'uuid': u.group(1) if u else '?',
                    'net': net.group(1) if net else '?',
                    'layer': lay.group(1) if lay else '?',
                    'bbox': (min(xs), min(ys), max(xs), max(ys)) if xs else None,
                    'fills': len(re.findall(r'\(filled_polygon', zb))})
    return out

def main():
    cmd, path = sys.argv[1], sys.argv[2]
    s = open(path).read()
    zs = zones(s)
    if cmd == 'list':
        for z in zs:
            bb = z['bbox']
            print(f"{z['uuid']}  net={z['net']:<8} layer={z['layer']:<8} "
                  f"outline=({bb[0]},{bb[1]})-({bb[2]},{bb[3]}) fills={z['fills']}")
        return
    if cmd != 'delete':
        sys.exit("unknown command")
    targets = sys.argv[3:]
    for u in targets:
        if s.count(u) != 1:
            sys.exit(f"REFUSED: uuid {u} appears {s.count(u)} times. "
                     f"Something references it. Delete it in the GUI.")
        if not any(z['uuid'] == u for z in zs):
            sys.exit(f"REFUSED: uuid {u} is not a zone.")
    stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
    bak = f"{path}.{stamp}.bak"
    shutil.copy2(path, bak)
    before = paren_balance(s)
    # delete from the end so earlier offsets stay valid
    for z in sorted([z for z in zs if z['uuid'] in targets], key=lambda z: -z['a']):
        s = s[:z['a']] + s[z['b']:]
    after = paren_balance(s)
    if after != before:
        sys.exit(f"REFUSED: paren balance changed {before} -> {after}. Nothing written.")
    open(path, 'w').write(s)
    print(f"backup: {bak}")
    print(f"deleted {len(targets)} zone(s). zones now: {len(zones(s))}. paren balance {after}")

main()
