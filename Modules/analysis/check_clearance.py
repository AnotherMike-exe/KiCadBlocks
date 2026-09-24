#!/usr/bin/env python3
"""Geometric clearance check for a KiCad 10 board.

Reports every track-to-pad and track-to-track pair on the same copper layer
that belongs to different nets and sits closer than the limit.

This is a planning aid. It does NOT replace KiCad DRC. It ignores zones,
net classes and custom rules, and it treats every pad as a rectangle.

Usage:  python3 check_clearance.py <board.kicad_pcb> [limit_mm]
"""
import re, math, sys

def blocks(src, tag):
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
        yield src[i:j+1]
        i = j

def rot(x, y, a):
    a = math.radians(a)
    c, s = math.cos(a), math.sin(a)
    return (x*c + y*s, -x*s + y*c)

def seg_point_dist(ax, ay, bx, by, px, py):
    dx, dy = bx-ax, by-ay
    L2 = dx*dx + dy*dy
    if L2 == 0:
        return math.hypot(px-ax, py-ay)
    t = max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy) / L2))
    return math.hypot(px - (ax+t*dx), py - (ay+t*dy))

def seg_seg_dist(a, b, c, d):
    def cross(o, p, q):
        return (p[0]-o[0])*(q[1]-o[1]) - (p[1]-o[1])*(q[0]-o[0])
    d1, d2 = cross(c, d, a), cross(c, d, b)
    d3, d4 = cross(a, b, c), cross(a, b, d)
    if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
        return 0.0
    return min(seg_point_dist(*a, *b, *c), seg_point_dist(*a, *b, *d),
               seg_point_dist(*c, *d, *a), seg_point_dist(*c, *d, *b))

def load(path):
    s = open(path).read()
    pads = []
    for fb in blocks(s, '\n\t(footprint '):
        at = re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', fb)
        fx, fy, fa = float(at.group(1)), float(at.group(2)), float(at.group(3) or 0)
        ref = re.search(r'\(property "Reference" "([^"]*)"', fb).group(1)
        for pb in blocks(fb, '\n\t\t(pad '):
            num = re.match(r'\n\t\t\(pad "([^"]*)"', pb).group(1)
            kind = re.match(r'\n\t\t\(pad "[^"]*" (\w+)', pb).group(1)
            pat = re.search(r'\n\t\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', pb)
            sz = re.search(r'\(size ([-\d.]+) ([-\d.]+)\)', pb)
            net = re.search(r'\(net "([^"]*)"\)', pb)
            lay = re.findall(r'"([FB]\.Cu|\*\.Cu|In\d\.Cu)"', pb)
            px, py = rot(float(pat.group(1)), float(pat.group(2)), fa)
            # A pad angle stored in a BOARD file is absolute: KiCad bakes the
            # footprint rotation into it. Only fall back to the footprint angle
            # when the pad carries none. Measured on KiCad 10.0.6, U1 pad 19:
            # footprint -90, pad 270, and the pad is wide in x, not tall in y.
            pa = (float(pat.group(3)) if pat.group(3) else fa) % 180
            w, h = float(sz.group(1)), float(sz.group(2))
            if abs(pa - 90) < 1:
                w, h = h, w
            layers = ['F.Cu', 'In1.Cu', 'In2.Cu', 'B.Cu'] if (kind != 'smd' or '*.Cu' in lay) else lay
            # A pad with no number AND no net is a paste or mask aperture, not
            # copper. U1's footprint carries four of them for the exposed pad's
            # paste windows. Counting them invents violations against the
            # thermal via array. Measured 2026-09-23.
            if not num and not (net and net.group(1)):
                continue
            if not lay:
                continue
            pads.append({'ref': f"{ref}.{num}", 'x': fx+px, 'y': fy+py, 'w': w, 'h': h,
                         'net': net.group(1) if net else '', 'layers': layers, 'thru': kind != 'smd'})
    segs = []
    for m in re.finditer(r'\(segment\s*\(start ([-\d.]+) ([-\d.]+)\)\s*\(end ([-\d.]+) ([-\d.]+)\)'
                         r'\s*\(width ([-\d.]+)\)\s*\(layer "([^"]+)"\)\s*\(net "([^"]*)"\)\s*\(uuid "([^"]+)"\)', s):
        segs.append({'a': (float(m.group(1)), float(m.group(2))),
                     'b': (float(m.group(3)), float(m.group(4))),
                     'w': float(m.group(5)), 'layer': m.group(6),
                     'net': m.group(7), 'uuid': m.group(8)})
    vias = []
    for vb in blocks(s, '\n\t(via'):
        at = re.search(r'\(at ([-\d.]+) ([-\d.]+)\)', vb)
        sz = re.search(r'\(size ([-\d.]+)\)', vb)
        net = re.search(r'\(net "([^"]*)"\)', vb)
        if at and sz:
            vias.append({'x': float(at.group(1)), 'y': float(at.group(2)),
                         'd': float(sz.group(1)), 'net': net.group(1) if net else ''})
    return pads, segs, vias

def main():
    path = sys.argv[1]
    limit = float(sys.argv[2]) if len(sys.argv) > 2 else 0.2
    pads, segs, vias = load(path)
    print(f"pads {len(pads)}  segments {len(segs)}  vias {len(vias)}  limit {limit} mm\n")
    hits = []
    for sg in segs:
        hw = sg['w'] / 2.0
        for p in pads:
            if p['net'] == sg['net'] or sg['layer'] not in p['layers']:
                continue
            hx, hy = p['w']/2.0, p['h']/2.0
            # distance from the segment to the pad rectangle, sampled on the rectangle border
            best = 1e9
            steps = 12
            for i in range(steps+1):
                t = i/steps
                for cx, cy in [(p['x']-hx + 2*hx*t, p['y']-hy), (p['x']-hx + 2*hx*t, p['y']+hy),
                               (p['x']-hx, p['y']-hy + 2*hy*t), (p['x']+hx, p['y']-hy + 2*hy*t)]:
                    best = min(best, seg_point_dist(*sg['a'], *sg['b'], cx, cy))
            gap = best - hw
            if gap < limit:
                hits.append((round(gap, 3), 'track-pad', sg['layer'], sg['net'], p['ref'], p['net'], sg['uuid']))
        for p in vias:
            if p['net'] == sg['net']:
                continue
            gap = seg_point_dist(*sg['a'], *sg['b'], p['x'], p['y']) - hw - p['d']/2.0
            if gap < limit:
                hits.append((round(gap, 3), 'track-via', sg['layer'], sg['net'], f"via@{p['x']},{p['y']}", p['net'], sg['uuid']))
    for i in range(len(segs)):
        for j in range(i+1, len(segs)):
            s1, s2 = segs[i], segs[j]
            if s1['net'] == s2['net'] or s1['layer'] != s2['layer']:
                continue
            gap = seg_seg_dist(s1['a'], s1['b'], s2['a'], s2['b']) - s1['w']/2.0 - s2['w']/2.0
            if gap < limit:
                hits.append((round(gap, 3), 'track-track', s1['layer'], s1['net'], s2['net'], '', s1['uuid']))
    hits.sort()
    if not hits:
        print("No violation under the limit.")
        return
    print(f"{len(hits)} pairs under {limit} mm:\n")
    for h in hits:
        print(f"  gap {h[0]:>7}  {h[1]:<12} {h[2]:<7} {h[3]:<18} vs {h[4]:<22} {h[5]:<18} {h[6][:8]}")

main()
