#!/usr/bin/env python3
"""Check planned routes against a board BEFORE writing them.

Reads the board's pads and existing tracks, adds planned segments and vias from
a JSON file, then reports every same-layer different-net pair under the limit.

JSON: {"moves":[[ref,x,y,rot],...],
       "segs":[[net,layer,x1,y1,x2,y2,width],...],
       "vias":[[net,x,y],...]}

Usage: python3 check_plan.py <board.kicad_pcb> <plan.json> [limit_mm]
"""
import json, sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("cc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_clearance.py"))

# re-use the loader by importing the module source without running main()
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "check_clearance.py")).read()
src = src.replace("\nmain()\n", "\n")
ns = {}
exec(compile(src, "check_clearance.py", "exec"), ns)
load, seg_point_dist, seg_seg_dist, rot = ns['load'], ns['seg_point_dist'], ns['seg_seg_dist'], ns['rot']

board, planfile = sys.argv[1], sys.argv[2]
limit = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2
plan = json.load(open(planfile))
pads, segs, vias = load(board)

# apply planned moves to the pad set
for ref, nx, ny, nrot in plan.get("moves", []):
    old = [p for p in pads if p['ref'].split('.')[0] == ref]
    if not old:
        print(f"  WARNING: move target {ref} not found")
        continue
    # recover the footprint origin from any pad is not possible; recompute from
    # the board is cheaper, so moves are checked by re-running after applying.
    print(f"  note: move {ref} -> ({nx},{ny},{nrot}) is NOT simulated; apply it first, then re-check")

planned = [{'a': (s[2], s[3]), 'b': (s[4], s[5]), 'w': s[6], 'layer': s[1], 'net': s[0], 'uuid': 'PLAN'}
           for s in plan.get("segs", [])]
pvias = [{'x': v[1], 'y': v[2], 'd': 0.8, 'net': v[0]} for v in plan.get("vias", [])]

allsegs = segs + planned
allvias = vias + pvias
print(f"board: pads {len(pads)} segs {len(segs)} vias {len(vias)}"
      f"   plan: segs {len(planned)} vias {len(pvias)}   limit {limit} mm\n")

hits = []
def pad_gap(sg, p):
    hx, hy = p['w']/2.0, p['h']/2.0
    best = 1e9
    for i in range(13):
        t = i/12
        for cx, cy in [(p['x']-hx+2*hx*t, p['y']-hy), (p['x']-hx+2*hx*t, p['y']+hy),
                       (p['x']-hx, p['y']-hy+2*hy*t), (p['x']+hx, p['y']-hy+2*hy*t)]:
            best = min(best, seg_point_dist(*sg['a'], *sg['b'], cx, cy))
    return best - sg['w']/2.0

for sg in allsegs:
    tag = 'PLAN' if sg['uuid'] == 'PLAN' else 'board'
    for p in pads:
        if p['net'] == sg['net'] or sg['layer'] not in p['layers']:
            continue
        g = pad_gap(sg, p)
        if g < limit:
            hits.append((round(g, 3), tag, 'track-pad', sg['layer'], sg['net'], p['ref'], p['net']))
    for v in allvias:
        if v['net'] == sg['net']:
            continue
        g = seg_point_dist(*sg['a'], *sg['b'], v['x'], v['y']) - sg['w']/2.0 - v['d']/2.0
        if g < limit:
            hits.append((round(g, 3), tag, 'track-via', sg['layer'], sg['net'], f"via {v['x']},{v['y']}", v['net']))
for i in range(len(allsegs)):
    for j in range(i+1, len(allsegs)):
        s1, s2 = allsegs[i], allsegs[j]
        if s1['net'] == s2['net'] or s1['layer'] != s2['layer']:
            continue
        g = seg_seg_dist(s1['a'], s1['b'], s2['a'], s2['b']) - s1['w']/2.0 - s2['w']/2.0
        if g < limit:
            tag = 'PLAN' if 'PLAN' in (s1['uuid'], s2['uuid']) else 'board'
            hits.append((round(g, 3), tag, 'track-track', s1['layer'], s1['net'], s2['net'],
                         f"{s1['a']}-{s1['b']} / {s2['a']}-{s2['b']}"))
for v in allvias:
    for p in pads:
        if p['net'] == v['net'] or not p['net']:
            continue
        hx, hy = p['w']/2.0, p['h']/2.0
        dx = max(abs(v['x']-p['x']) - hx, 0); dy = max(abs(v['y']-p['y']) - hy, 0)
        g = math.hypot(dx, dy) - v['d']/2.0
        if g < limit:
            hits.append((round(g, 3), 'PLAN', 'via-pad', 'all', v['net'], p['ref'], p['net']))
hits.sort()
if not hits:
    print("No violation under the limit.")
else:
    print(f"{len(hits)} pairs under {limit} mm:\n")
    for h in hits:
        print(f"  gap {h[0]:>7}  {h[1]:<5} {h[2]:<12} {h[3]:<7} {h[4]:<18} vs {h[5]:<26} {h[6]}")
