#!/usr/bin/env python3
"""Report footprint courtyard overlaps on a KiCad 10 board.

Courtyards come from the fp_* graphics the board file embeds in each footprint.
Only a footprint that carries none falls back to its library .kicad_mod, found
through the global fp-lib-table and the project fp-lib-table next to the board.
Board bounds come from the board's own Edge.Cuts graphics.

Usage: python3 check_courtyards.py <board.kicad_pcb> [warn_gap_mm]
"""
import re, math, sys, os, json
d = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(d, "check_clearance.py")).read().replace("\nmain()\n", "\n")
ns = {}
exec(compile(src, "check_clearance.py", "exec"), ns)
blocks, rot = ns['blocks'], ns['rot']

KICAD_CFG = os.path.expanduser("~/Library/Preferences/kicad/10.0")
GLOBAL_TABLE = os.path.join(KICAD_CFG, "fp-lib-table")
KICAD_COMMON = os.path.join(KICAD_CFG, "kicad_common.json")
DEFAULT_ENV = {
    "PLUM_SOLUTIONS": ("/Users/michaelprice/Library/Application Support/Mountain Duck/Volumes.noindex/"
                       "SyncIn.localized/personal/Plum Solutions/KiCAD"),
    "KICAD10_FOOTPRINT_DIR": "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints",
}
PT = r'\((?:start|end|xy|center|mid) ([-\d.]+) ([-\d.]+)\)'

def kicad_env(common=KICAD_COMMON):
    """Path variables: fallbacks, then kicad_common.json, then the process environment."""
    env = dict(DEFAULT_ENV)
    try:
        env.update(json.load(open(common)).get("environment", {}).get("vars") or {})
    except (OSError, ValueError):
        pass
    env.update({k: os.environ[k] for k in env if k in os.environ})
    return env

def expand(uri, env):
    return re.sub(r'\$\{(\w+)\}', lambda m: env.get(m.group(1), m.group(0)), uri)

def read_table(path, env, seen=None):
    """{nickname: .pretty dir} from one fp-lib-table. A "Table" row nests another table."""
    seen = seen if seen is not None else set()
    if not os.path.isfile(path) or path in seen:
        return {}
    seen.add(path)
    libs = {}
    for m in re.finditer(r'\(lib \(name "([^"]+)"\)\s*\(type "([^"]+)"\)\s*\(uri "([^"]*)"\)', open(path).read()):
        name, kind, uri = m.group(1), m.group(2), expand(m.group(3), env)
        if kind == "Table":
            for k, v in read_table(uri, env, seen).items():
                libs.setdefault(k, v)
        else:
            libs.setdefault(name, uri)
    return libs

def lib_table(board, global_table=GLOBAL_TABLE, env=None):
    # The global row wins on a duplicate nickname. Measured on KiCad 10: a project
    # row does not shadow a global one.
    env = dict(env if env is not None else kicad_env())
    env["KIPRJMOD"] = os.path.dirname(os.path.abspath(board))
    libs = read_table(os.path.join(env["KIPRJMOD"], "fp-lib-table"), env)
    libs.update(read_table(global_table, env))
    return libs

def crtyd_points(text, tag, layers=("F.CrtYd", "B.CrtYd")):
    """Every outline point of the courtyard graphics in a footprint body.
    tag is the indented '(fp_' prefix: one tab deeper in a board than in a .kicad_mod."""
    pts = []
    for g in blocks(text, tag):
        lay = re.search(r'\(layer "([^"]+)"\)', g)
        if not lay or lay.group(1) not in layers:
            continue
        p = [(float(a), float(b)) for a, b in re.findall(PT, g)]
        if g.lstrip().startswith('(fp_circle') and len(p) == 2:
            (cx, cy), (ex, ey) = p
            r = math.hypot(ex-cx, ey-cy)
            p = [(cx-r, cy-r), (cx+r, cy+r)]
        pts += p
    return pts

cache = {}
def lib_points(lib, libs):
    if lib not in cache:
        l, n = lib.split(':', 1)
        path = os.path.join(libs.get(l, ''), n + '.kicad_mod')
        # Put every item on its own tab-indented line: hand-written footprints use
        # two spaces and one line per item, and blocks() needs a fixed prefix.
        text = re.sub(r'\s*\(fp_', '\n\t(fp_', open(path).read()) if os.path.isfile(path) else ''
        cache[lib] = crtyd_points(text, '\n\t(fp_', ("F.CrtYd",)) or None
    return cache[lib]

def footprint_boxes(s, libs):
    """({ref: (x0, y0, x1, y1)}, [(ref, lib) with no courtyard found])."""
    boxes, missing = {}, []
    for fb in blocks(s, '\n\t(footprint '):
        lib = re.search(r'\(footprint "([^"]+)"', fb).group(1)
        at = re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', fb)
        ref = re.search(r'\(property "Reference" "([^"]*)"', fb).group(1)
        x, y, a = float(at.group(1)), float(at.group(2)), float(at.group(3) or 0)
        # The board copy is already flipped for a back-side part; use it when present.
        pts = crtyd_points(fb, '\n\t\t(fp_')
        if not pts:
            pts = lib_points(lib, libs)
            if pts and re.search(r'\n\t\t\(layer "B\.Cu"\)', fb):
                pts = [(-px, py) for px, py in pts]   # approximate: mirror the library copy in x
        if not pts:
            missing.append((ref, lib))
            continue
        pts = [rot(px, py, a) for px, py in pts]
        boxes[ref] = (x+min(p[0] for p in pts), y+min(p[1] for p in pts),
                      x+max(p[0] for p in pts), y+max(p[1] for p in pts))
    return boxes, missing

def board_bounds(s):
    """Bounding box of the top-level Edge.Cuts graphics, or None when there are none."""
    xs, ys = [], []
    for g in blocks(s, '\n\t(gr_'):
        if '(layer "Edge.Cuts")' not in g:
            continue
        p = [(float(a), float(b)) for a, b in re.findall(PT, g)]
        if g.startswith('\n\t(gr_circle') and len(p) == 2:
            (cx, cy), (ex, ey) = p
            r = math.hypot(ex-cx, ey-cy)
            p = [(cx-r, cy-r), (cx+r, cy+r)]
        xs += [q[0] for q in p]; ys += [q[1] for q in p]
    return (min(xs), min(ys), max(xs), max(ys)) if xs else None

def compare(boxes, warn):
    refs = sorted(boxes)
    bad, tight = [], []
    for i in range(len(refs)):
        for j in range(i+1, len(refs)):
            a, b = boxes[refs[i]], boxes[refs[j]]
            ox = min(a[2], b[2]) - max(a[0], b[0]); oy = min(a[3], b[3]) - max(a[1], b[1])
            if ox > 0.001 and oy > 0.001:
                bad.append((refs[i], refs[j], round(ox, 3), round(oy, 3)))
            else:
                g = max(max(a[0], b[0]) - min(a[2], b[2]), max(a[1], b[1]) - min(a[3], b[3]))
                if 0 <= g < warn:
                    tight.append((refs[i], refs[j], round(g, 3)))
    return bad, tight

def off_board(boxes, bounds):
    x0, y0, x1, y1 = bounds
    return [(r, b) for r, b in boxes.items() if b[0] < x0 or b[2] > x1 or b[1] < y0 or b[3] > y1]

def main(argv):
    board = argv[1]
    warn = float(argv[2]) if len(argv) > 2 else 0.05
    s = open(board).read()
    boxes, missing = footprint_boxes(s, lib_table(board))
    bad, tight = compare(boxes, warn)
    print(f"{len(boxes)} footprints")
    for ref, lib in missing:
        print(f"  note: {ref} ({lib}) has no courtyard on the board or in its library; skipped")
    print("overlaps:", bad or "NONE")
    print(f"gaps under {warn}:", tight or "NONE")
    bounds = board_bounds(s)
    if bounds is None:
        print("  note: no Edge.Cuts graphics on the board; off-board check skipped")
    else:
        print("off board:", off_board(boxes, bounds) or "NONE")

if __name__ == "__main__":
    main(sys.argv)
