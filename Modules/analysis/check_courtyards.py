#!/usr/bin/env python3
"""Report footprint courtyard overlaps on a KiCad 10 board.

Usage: python3 check_courtyards.py <board.kicad_pcb> [warn_gap_mm]
"""
import re, math, sys, os
d = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(d, "check_clearance.py")).read().replace("\nmain()\n", "\n")
ns = {}
exec(compile(src, "check_clearance.py", "exec"), ns)
blocks, rot = ns['blocks'], ns['rot']

KI = "/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints"
PLUM = ("/Users/michaelprice/Library/Application Support/Mountain Duck/Volumes.noindex/"
        "SyncIn.localized/personal/Plum Solutions/KiCAD/Footprints/PlumRFBridge.pretty")

def fp_path(lib):
    l, n = lib.split(':')
    return os.path.join(PLUM, n + '.kicad_mod') if l == 'PlumRFBridge' else os.path.join(KI, l + '.pretty', n + '.kicad_mod')

cache = {}
def crtyd(lib):
    if lib in cache:
        return cache[lib]
    t = open(fp_path(lib)).read()
    xs, ys = [], []
    for blk in re.findall(r'\(fp_(?:line|rect|poly|circle|arc)[\s\S]{0,600}?\(layer "F\.CrtYd"\)', t):
        for a, b in re.findall(r'\((?:start|end|xy|center|mid) ([-\d.]+) ([-\d.]+)\)', blk):
            xs.append(float(a)); ys.append(float(b))
    cache[lib] = (min(xs), min(ys), max(xs), max(ys)) if xs else None
    return cache[lib]

board = sys.argv[1]
warn = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
s = open(board).read()
boxes = {}
for fb in blocks(s, '\n\t(footprint '):
    lib = re.search(r'\(footprint "([^"]+)"', fb).group(1)
    at = re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', fb)
    ref = re.search(r'\(property "Reference" "([^"]*)"', fb).group(1)
    x, y, a = float(at.group(1)), float(at.group(2)), float(at.group(3) or 0)
    c = crtyd(lib)
    if not c:
        continue
    pts = [rot(px, py, a) for px, py in [(c[0], c[1]), (c[2], c[1]), (c[2], c[3]), (c[0], c[3])]]
    boxes[ref] = (x+min(p[0] for p in pts), y+min(p[1] for p in pts),
                  x+max(p[0] for p in pts), y+max(p[1] for p in pts))
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
print(f"{len(boxes)} footprints")
print("overlaps:", bad or "NONE")
print(f"gaps under {warn}:", tight or "NONE")
off = [(r, b) for r, b in boxes.items() if b[0] < 100 or b[2] > 156 or b[1] < 50 or b[3] > 134]
print("off board:", off or "NONE")
