#!/usr/bin/env python3
"""Check a 3D model before it is printed or sent to a print service.

Standard library only, so it runs on any machine with Python 3.8+.

Reads STL (binary or text), OBJ and 3MF. Reports:
  - size in mm, with a units sanity check and an optional printer-bed fit check
  - whether the mesh is one sealed solid (watertight, consistent faces)
  - how many separate pieces it contains
  - volume, surface area and an estimated weight for the chosen material
  - for each of the 6 flat orientations: bed contact area, area that needs
    support (overhangs steeper than 45 degrees) and print height
  - an optional PNG preview: top, front, 3D from above and 3D from below,
    with faces that need support drawn in red
  - optional cross-sections that measure holes, clips and outlines at a height
  - optional line probes that measure walls, notches and slots along a line

Usage:
  python3 check_print.py part.stl
  python3 check_print.py part.3mf --material PETG --bed 220x220x250 --preview part.png
  python3 check_print.py base.stl lid.stl --section z=4 --probe z=5,y=40
  python3 check_print.py part.stl --json
"""

import argparse
import json
import math
import os
import re
import struct
import sys
import zipfile
import zlib
import xml.etree.ElementTree as ET

DENSITY = {  # g/cm3, typical values
    "PLA": 1.24, "PETG": 1.27, "ABS": 1.04, "ASA": 1.07, "TPU": 1.21,
    "NYLON": 1.14, "PA12": 1.01, "RESIN": 1.12, "PC": 1.20,
}
OVERHANG_COS = math.cos(math.radians(45))


# ---------------------------------------------------------------- loading

def load_stl(path):
    data = open(path, "rb").read()
    if len(data) >= 84:
        n = struct.unpack_from("<I", data, 80)[0]
        if 84 + 50 * n == len(data):
            tris = []
            for rec in struct.iter_unpack("<12fH", data[84:84 + 50 * n]):
                tris.append((rec[3:6], rec[6:9], rec[9:12]))
            return tris, []
    text = data.decode("latin-1")
    nums = re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", text)
    verts = [(float(a), float(b), float(c)) for a, b, c in nums]
    if not verts or len(verts) % 3:
        raise ValueError("could not read this STL (not binary, and no text vertices found)")
    return [tuple(verts[i:i + 3]) for i in range(0, len(verts), 3)], []


def load_obj(path):
    verts, tris = [], []
    for line in open(path, encoding="latin-1"):
        parts = line.split()
        if not parts:
            continue
        if parts[0] == "v":
            verts.append(tuple(float(x) for x in parts[1:4]))
        elif parts[0] == "f":
            idx = []
            for p in parts[1:]:
                i = int(p.split("/")[0])
                idx.append(i - 1 if i > 0 else len(verts) + i)
            for k in range(1, len(idx) - 1):  # fan-triangulate polygons
                tris.append((verts[idx[0]], verts[idx[k]], verts[idx[k + 1]]))
    return tris, []


UNIT_SCALE = {"micron": 0.001, "millimeter": 1.0, "centimeter": 10.0,
              "inch": 25.4, "foot": 304.8, "meter": 1000.0}


def _mat(text):
    if not text:
        return None
    v = [float(x) for x in text.split()]
    return [[v[0], v[1], v[2]], [v[3], v[4], v[5]], [v[6], v[7], v[8]], [v[9], v[10], v[11]]]


def _mul(a, b):
    """Compose 3MF transforms: apply a, then b (row-vector convention)."""
    if a is None:
        return b
    if b is None:
        return a
    out = []
    for r in range(3):
        out.append([sum(a[r][k] * b[k][c] for k in range(3)) for c in range(3)])
    out.append([sum(a[3][k] * b[k][c] for k in range(3)) + b[3][c] for c in range(3)])
    return out


def _apply(m, p):
    if m is None:
        return p
    x, y, z = p
    return tuple(x * m[0][c] + y * m[1][c] + z * m[2][c] + m[3][c] for c in range(3))


def load_3mf(path):
    notes = []
    z = zipfile.ZipFile(path)
    models = {}  # path -> (unit scale, {id: element})
    for name in z.namelist():
        if name.lower().endswith(".model"):
            root = ET.fromstring(z.read(name))
            scale = UNIT_SCALE.get(root.get("unit", "millimeter"), 1.0)
            objs = {}
            for el in root.iter():
                if el.tag.endswith("}object"):
                    objs[el.get("id")] = el
            models["/" + name.lstrip("/")] = (scale, objs, root)
    main = next((k for k in models if k.lower().endswith("3d/3dmodel.model")), None)
    if main is None:
        raise ValueError("no 3D/3dmodel.model inside this 3MF")

    tris = []

    def emit(model_path, oid, m, depth=0):
        if depth > 20:
            return
        scale, objs, _ = models.get(model_path, (1.0, {}, None))
        obj = objs.get(oid)
        if obj is None:
            notes.append(f"missing object {oid} in {model_path}")
            return
        for child in obj:
            tag = child.tag.split("}")[-1]
            if tag == "mesh":
                vs = []
                for el in child.iter():
                    t = el.tag.split("}")[-1]
                    if t == "vertex":
                        p = (float(el.get("x")) * scale, float(el.get("y")) * scale,
                             float(el.get("z")) * scale)
                        vs.append(_apply(m, p))
                    elif t == "triangle":
                        tris.append((vs[int(el.get("v1"))], vs[int(el.get("v2"))],
                                     vs[int(el.get("v3"))]))
            elif tag == "components":
                for comp in child:
                    sub_path = model_path
                    for k, v in comp.attrib.items():
                        if k.endswith("}path") or k == "path":
                            sub_path = "/" + v.lstrip("/")
                    emit(sub_path, comp.get("objectid"),
                         _mul(_mat(comp.get("transform")), m), depth + 1)

    _, _, root = models[main]
    items = [el for el in root.iter() if el.tag.endswith("}item")]
    if not items:
        raise ValueError("this 3MF has no build items")
    for it in items:
        emit(main, it.get("objectid"), _mat(it.get("transform")))
    if len(items) > 1:
        notes.append(f"{len(items)} objects on the build plate; they are checked together")
    return tris, notes


def load(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".stl":
        return load_stl(path)
    if ext == ".obj":
        return load_obj(path)
    if ext == ".3mf":
        return load_3mf(path)
    raise ValueError(f"unsupported file type {ext!r}; use STL, OBJ or 3MF "
                     "(export STEP files to STL from the CAD program first)")


# ---------------------------------------------------------------- geometry

def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def build_mesh(raw_tris, eps=1e-4):
    index, verts, faces = {}, [], []
    for tri in raw_tris:
        ids = []
        for p in tri:
            key = (round(p[0] / eps), round(p[1] / eps), round(p[2] / eps))
            i = index.get(key)
            if i is None:
                i = index[key] = len(verts)
                verts.append(tuple(float(c) for c in p))
            ids.append(i)
        if len(set(ids)) == 3:
            faces.append(tuple(ids))
    return verts, faces


def analyse(verts, faces):
    normals, areas = [], []
    volume6 = 0.0
    for a, b, c in faces:
        va, vb, vc = verts[a], verts[b], verts[c]
        n = cross(sub(vb, va), sub(vc, va))
        ln = math.sqrt(dot(n, n))
        areas.append(ln / 2)
        normals.append((n[0] / ln, n[1] / ln, n[2] / ln) if ln > 0 else (0.0, 0.0, 0.0))
        volume6 += dot(va, cross(vb, vc))
    volume = volume6 / 6.0
    inverted = volume < 0
    if inverted:
        normals = [(-x, -y, -z) for x, y, z in normals]
        volume = -volume

    edge_count, directed = {}, {}
    for a, b, c in faces:
        for u, v in ((a, b), (b, c), (c, a)):
            k = (u, v) if u < v else (v, u)
            edge_count[k] = edge_count.get(k, 0) + 1
            directed[(u, v)] = directed.get((u, v), 0) + 1
    open_edges = sum(1 for n in edge_count.values() if n == 1)
    nonmanifold = sum(1 for n in edge_count.values() if n > 2)
    flipped = sum(1 for n in directed.values() if n > 1)

    # separate pieces: union-find over shared vertices
    parent = list(range(len(verts)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b, c in faces:
        ra, rb, rc = find(a), find(b), find(c)
        parent[rb] = ra
        parent[find(rc)] = ra
    shells = {}
    for f in faces:
        shells.setdefault(find(f[0]), []).append(f)

    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    zs = [v[2] for v in verts]
    bbox_min = (min(xs), min(ys), min(zs))
    bbox_max = (max(xs), max(ys), max(zs))

    shell_sizes = []
    for fs in shells.values():
        ids = {i for f in fs for i in f}
        sx = [verts[i][0] for i in ids]
        sy = [verts[i][1] for i in ids]
        sz = [verts[i][2] for i in ids]
        shell_sizes.append(sorted([max(sx) - min(sx), max(sy) - min(sy), max(sz) - min(sz)]))

    return {
        "normals": normals, "areas": areas, "volume_mm3": volume,
        "area_mm2": sum(areas), "inverted": inverted,
        "open_edges": open_edges, "nonmanifold_edges": nonmanifold,
        "flipped_edges": flipped, "shells": len(shells), "shell_sizes": shell_sizes,
        "bbox_min": bbox_min, "bbox_max": bbox_max,
    }


ORIENTATIONS = [  # (label, direction that points DOWN onto the bed)
    ("as saved (-Z down)", (0, 0, -1)), ("+Z down", (0, 0, 1)),
    ("-Y down", (0, -1, 0)), ("+Y down", (0, 1, 0)),
    ("-X down", (-1, 0, 0)), ("+X down", (1, 0, 0)),
]


def orientation_table(verts, faces, normals, areas, tol=0.05):
    rows = []
    for label, d in ORIENTATIONS:
        proj = [dot(v, d) for v in verts]
        bottom = max(proj)  # the plane touching the bed
        height = bottom - min(proj)
        contact = overhang = 0.0
        for (a, b, c), n, ar in zip(faces, normals, areas):
            facing = dot(n, d)
            if facing > OVERHANG_COS:
                if facing > 0.99 and min(proj[a], proj[b], proj[c]) > bottom - tol:
                    contact += ar
                else:
                    overhang += ar
        rows.append({"orientation": label, "down": d, "height_mm": height,
                     "bed_contact_mm2": contact, "needs_support_mm2": overhang})
    return rows


# ---------------------------------------------------------------- cross-section

def _inside(pt, poly):
    x, y = pt
    inside = False
    j = len(poly) - 1
    for i in range(len(poly)):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def section(verts, faces, axis, value):
    """Cut the mesh with a flat plane and return the closed outlines found there.

    Each outline reports whether it is material or a hole, its size, centre and,
    for round outlines, the diameter. Used to check fit-critical sizes such as
    clips, screw holes and board pockets.
    """
    ax = "xyz".index(axis)
    u, v = [i for i in range(3) if i != ax]
    value += 1e-6  # avoid vertices exactly on the plane
    segs = []
    for f in faces:
        pts = [verts[i] for i in f]
        d = [p[ax] - value for p in pts]
        cross_pts = []
        for i in range(3):
            a, b = pts[i], pts[(i + 1) % 3]
            da, db = d[i], d[(i + 1) % 3]
            if (da < 0) != (db < 0):
                t = da / (da - db)
                cross_pts.append((a[u] + t * (b[u] - a[u]), a[v] + t * (b[v] - a[v])))
        if len(cross_pts) == 2:
            segs.append(tuple(cross_pts))

    key = lambda p: (round(p[0], 4), round(p[1], 4))
    adj = {}
    for a, b in segs:
        ka, kb = key(a), key(b)
        if ka == kb:
            continue
        adj.setdefault(ka, []).append(kb)
        adj.setdefault(kb, []).append(ka)
    loops, seen = [], set()
    for start in adj:
        if start in seen:
            continue
        loop, prev, cur = [start], None, start
        seen.add(start)
        while True:
            nxt = [n for n in adj[cur] if n != prev and (n not in seen or (n == start and len(loop) > 2))]
            if not nxt:
                break
            prev, cur = cur, nxt[0]
            if cur == start:
                break
            seen.add(cur)
            loop.append(cur)
        if len(loop) >= 3:
            loops.append(loop)

    out = []
    for i, lp in enumerate(loops):
        area = 0.0
        per = 0.0
        for k in range(len(lp)):
            x0, y0 = lp[k]
            x1, y1 = lp[(k + 1) % len(lp)]
            area += x0 * y1 - x1 * y0
            per += math.hypot(x1 - x0, y1 - y0)
        area = abs(area) / 2
        xs = [p[0] for p in lp]
        ys = [p[1] for p in lp]
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        if w < 0.01 and h < 0.01:
            continue  # the plane only grazes a tip
        depth = sum(1 for j, other in enumerate(loops) if j != i and _inside(lp[0], other))
        entry = {"kind": "hole" if depth % 2 else "material", "size": [round(w, 2), round(h, 2)],
                 "centre": [round((max(xs) + min(xs)) / 2, 2), round((max(ys) + min(ys)) / 2, 2)],
                 "area_mm2": round(area, 2)}
        if w > 0 and 0.9 < h / w < 1.1:
            r = (w + h) / 4
            if 0.85 < area / (math.pi * r * r) < 1.08:
                entry["round_diameter"] = round(2 * math.sqrt(area / math.pi), 2)
        c = ((max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2)
        roundish = w > 0 and h > 0 and 0.85 < h / w < 1.18
        if entry["kind"] == "material" and roundish and not _inside(c, lp):
            # C-shaped clip or open ring: report the clear space around its centre.
            # Rectangles and long walls are skipped: use --probe to measure those.
            best = float("inf")
            for k in range(len(lp)):
                (x0, y0), (x1, y1) = lp[k], lp[(k + 1) % len(lp)]
                dx, dy = x1 - x0, y1 - y0
                L = dx * dx + dy * dy
                t = 0.0 if L == 0 else max(0.0, min(1.0, ((c[0] - x0) * dx + (c[1] - y0) * dy) / L))
                best = min(best, math.hypot(x0 + t * dx - c[0], y0 + t * dy - c[1]))
            entry["clear_centre_diameter"] = round(2 * best, 2)
        out.append(entry)
    out.sort(key=lambda e: -e["area_mm2"])
    return out, "xyz"[u], "xyz"[v]


# ---------------------------------------------------------------- preview

def _rot(yaw_deg, pitch_deg):
    y, p = math.radians(yaw_deg), math.radians(pitch_deg)
    rz = [[math.cos(y), -math.sin(y), 0], [math.sin(y), math.cos(y), 0], [0, 0, 1]]
    rx = [[1, 0, 0], [0, math.cos(p), -math.sin(p)], [0, math.sin(p), math.cos(p)]]
    return [[sum(rx[i][k] * rz[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def _tf(m, v):
    return (m[0][0] * v[0] + m[0][1] * v[1] + m[0][2] * v[2],
            m[1][0] * v[0] + m[1][1] * v[1] + m[1][2] * v[2],
            m[2][0] * v[0] + m[2][1] * v[1] + m[2][2] * v[2])


def render_view(tv, faces, normals, support, rot, size, cull, s):
    """Orthographic z-buffer render of pre-rotated vertices at scale s (px per mm)."""
    xs = [v[0] for v in tv]
    ys = [v[1] for v in tv]
    cx, cy = (max(xs) + min(xs)) / 2, (max(ys) + min(ys)) / 2
    sp = [((x - cx) * s + size / 2, size / 2 - (y - cy) * s, z) for x, y, z in tv]
    bg = (246, 246, 244)
    img = [[bg] * size for _ in range(size)]
    zb = [[-1e30] * size for _ in range(size)]
    light = (0.35, 0.45, 0.82)
    for fi, (a, b, c) in enumerate(faces):
        n = _tf(rot, normals[fi])
        if cull and n[2] <= 0:
            continue
        shade = 0.30 + 0.70 * abs(dot(n, light))
        base = (205, 70, 60) if support[fi] else (95, 135, 185)
        col = tuple(min(255, int(ch * shade + 25)) for ch in base)
        (x0, y0, z0), (x1, y1, z1), (x2, y2, z2) = sp[a], sp[b], sp[c]
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-12:
            continue
        lo_x, hi_x = max(0, int(min(x0, x1, x2))), min(size - 1, int(max(x0, x1, x2)) + 1)
        lo_y, hi_y = max(0, int(min(y0, y1, y2))), min(size - 1, int(max(y0, y1, y2)) + 1)
        for py in range(lo_y, hi_y + 1):
            fy = py + 0.5
            row, zrow = img[py], zb[py]
            for px in range(lo_x, hi_x + 1):
                fx = px + 0.5
                w0 = ((y1 - y2) * (fx - x2) + (x2 - x1) * (fy - y2)) / den
                w1 = ((y2 - y0) * (fx - x2) + (x0 - x2) * (fy - y2)) / den
                w2 = 1 - w0 - w1
                if w0 < -1e-6 or w1 < -1e-6 or w2 < -1e-6:
                    continue
                z = w0 * z0 + w1 * z1 + w2 * z2
                if z > zrow[px]:
                    zrow[px] = z
                    row[px] = col
    return img


def write_png(path, rows):
    h, w = len(rows), len(rows[0])
    raw = bytearray()
    for r in rows:
        raw.append(0)
        for px in r:
            raw.extend(px)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))
    open(path, "wb").write(png)


def preview(path, verts, faces, normals, support, cull, size=300):
    """Four views at one shared scale, each with a scale bar. Returns the bar length in mm."""
    xs = [v[0] for v in verts]
    ys = [v[1] for v in verts]
    long_x = (max(xs) - min(xs)) >= (max(ys) - min(ys))
    views = [_rot(0, 0),                              # top: looking down
             _rot(0 if long_x else -90, -90),         # front: facing the longer side
             _rot(-35, -60),                          # 3D view from above
             _rot(-35, -120)]                         # 3D view from below (shows support areas)
    tvs = [[_tf(r, v) for v in verts] for r in views]
    span = max(max(max(p[k] for p in tv) - min(p[k] for p in tv) for k in (0, 1)) for tv in tvs) or 1.0
    s = size * 0.86 / span
    bar = next((L for L in (0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000) if L * s >= 40), 1000)
    imgs = []
    for tv, r in zip(tvs, views):
        img = render_view(tv, faces, normals, support, r, size, cull, s)
        y0, x0, x1 = size - 10, 10, min(size - 2, 10 + int(round(bar * s)))
        for x in range(x0, x1 + 1):
            img[y0][x] = img[y0 - 1][x] = (60, 60, 60)
        for x in (x0, x1):
            for y in range(y0 - 5, y0 + 1):
                img[y][x] = (60, 60, 60)
        imgs.append(img)
    gap = [(220, 220, 216)] * 4
    rows = []
    for y in range(size):
        row = list(imgs[0][y])
        for img in imgs[1:]:
            row += gap + img[y]
        rows.append(row)
    write_png(path, rows)
    return bar


# ---------------------------------------------------------------- line probe

def probe(verts, faces, fixed):
    """Measure along a straight line parallel to one axis.

    `fixed` maps two axis indices to their values; the line runs along the third.
    Returns the solid and empty stretches where the line passes through the part,
    which shows notches, slots and wall thicknesses that a section outline hides.
    """
    free = [a for a in range(3) if a not in fixed][0]
    (a1, v1), (a2, v2) = sorted(fixed.items())
    v1 += 1.1e-6  # avoid passing exactly through edges and vertices
    v2 += 1.7e-6
    hits = []
    for f in faces:
        P = [verts[i] for i in f]
        x0, y0, x1, y1, x2, y2 = P[0][a1], P[0][a2], P[1][a1], P[1][a2], P[2][a1], P[2][a2]
        den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
        if abs(den) < 1e-12:
            continue
        w0 = ((y1 - y2) * (v1 - x2) + (x2 - x1) * (v2 - y2)) / den
        w1 = ((y2 - y0) * (v1 - x2) + (x0 - x2) * (v2 - y2)) / den
        w2 = 1 - w0 - w1
        if w0 < 0 or w1 < 0 or w2 < 0:
            continue
        hits.append(w0 * P[0][free] + w1 * P[1][free] + w2 * P[2][free])
    hits.sort()
    clean = []
    for h in hits:
        if not clean or h - clean[-1] > 1e-4:
            clean.append(h)
    solids = [(clean[i], clean[i + 1]) for i in range(0, len(clean) - 1, 2)]
    stretches = []
    for i, (a, b) in enumerate(solids):
        if i:
            stretches.append({"kind": "gap", "from": round(solids[i - 1][1], 2), "to": round(a, 2),
                              "length": round(a - solids[i - 1][1], 2)})
        stretches.append({"kind": "solid", "from": round(a, 2), "to": round(b, 2), "length": round(b - a, 2)})
    return stretches, "xyz"[free], len(clean) % 2 == 1


# ---------------------------------------------------------------- report

def parse_dims(text):
    parts = [float(x) for x in re.split(r"[x×*, ]+", text.strip()) if x]
    if len(parts) != 3:
        raise argparse.ArgumentTypeError("use WIDTHxDEPTHxHEIGHT in mm, e.g. 220x220x250")
    return parts


def check(path, args, preview_path):
    raw, notes = load(path)
    if not raw:
        raise ValueError("no triangles found")
    verts, faces = build_mesh(raw)
    info = analyse(verts, faces)
    table = orientation_table(verts, faces, info["normals"], info["areas"])
    size = [info["bbox_max"][i] - info["bbox_min"][i] for i in range(3)]

    mat = args.material.upper()
    warnings = list(notes)
    if mat not in DENSITY:
        warnings.append(f"unknown material {mat!r}; the weight uses PLA's density")
    dens = DENSITY.get(mat, 1.24)
    vol_cm3 = info["volume_mm3"] / 1000
    solid_g = vol_cm3 * dens
    # rough FDM estimate: ~1.2 mm of solid skin over the surface, infill inside
    shell_cm3 = min(vol_cm3, info["area_mm2"] * 1.2 / 1000)
    printed_g = (shell_cm3 + (vol_cm3 - shell_cm3) * args.infill / 100) * dens
    all_solid = shell_cm3 >= vol_cm3 * 0.999

    sealed = (info["open_edges"] == 0 and info["nonmanifold_edges"] == 0
              and info["flipped_edges"] == 0)
    if not sealed:
        warnings.append(
            f"not one sealed solid: {info['open_edges']} open edges, "
            f"{info['nonmanifold_edges']} edges shared by 3+ faces, {info['flipped_edges']} flipped. "
            "Most services and slicers repair small holes; for a large count, regenerate or repair the file.")
    if info["inverted"]:
        warnings.append("faces point inward (inside-out); the check corrected for it, but repair before ordering")
    if max(size) < 3:
        warnings.append(f"largest side is {max(size):.2f} — the file may be in metres or inches; "
                        "check the units before ordering")
    if max(size) > 1500:
        warnings.append(f"largest side is {max(size):.0f} mm — the file may be in microns; check the units")
    if info["shells"] > 1:
        tiny = sum(1 for s in info["shell_sizes"] if s[2] < 1.0)
        warnings.append(f"{info['shells']} separate pieces in one file"
                        + (f", {tiny} of them under 1 mm (likely stray fragments)" if tiny else "")
                        + ". Services often charge per piece; confirm this is intended.")
    thin = [s for s in info["shell_sizes"] if s[0] < 0.8 and s[2] >= 1.0]
    if thin:
        warnings.append(f"{len(thin)} piece(s) are thinner than 0.8 mm overall; "
                        "a 0.4 mm nozzle can't print that well")
    if args.bed:
        bed = sorted(args.bed)
        if not all(a <= b for a, b in zip(sorted(size), bed)):
            warnings.append(f"too big for a {args.bed[0]:g}x{args.bed[1]:g}x{args.bed[2]:g} mm bed in any orientation")
    current = table[0]
    if current["needs_support_mm2"] > 0.05 * info["area_mm2"]:
        warnings.append("more than 5% of the surface faces down as saved and may need support; "
                        "see the orientation table")
    if current["bed_contact_mm2"] < 20:
        warnings.append("almost nothing touches the bed as saved; rotate it, or ask the service to orient it")

    def score(r):  # more contact, less support, lower height
        return r["bed_contact_mm2"] - 3 * r["needs_support_mm2"] - 0.5 * r["height_mm"]
    best = max(table, key=score)

    result = {
        "file": path, "triangles": len(faces),
        "size_mm": [round(x, 2) for x in size], "sealed_solid": sealed,
        "pieces": info["shells"], "volume_cm3": round(vol_cm3, 2),
        "surface_area_mm2": round(info["area_mm2"], 1), "material": mat,
        "solid_weight_g": round(solid_g, 1), "printed_weight_g_est": round(printed_g, 1),
        "thin_walls_print_solid": all_solid,
        "orientations": [{k: (round(v, 1) if isinstance(v, float) else v) for k, v in r.items()}
                         for r in table],
        "suggested_orientation": best["orientation"], "warnings": warnings,
    }

    sections = []
    for spec in args.section or []:
        m = re.fullmatch(r"\s*([xyzXYZ])\s*=\s*(-?[\d.]+)\s*", spec)
        if not m:
            raise ValueError(f"--section expects AXIS=MM such as z=3, got {spec!r}")
        axis, val = m.group(1).lower(), float(m.group(2))
        loops, ua, va = section(verts, faces, axis, val)
        sections.append({"plane": f"{axis}={val:g}", "axes": f"{ua},{va}", "outlines": loops})
    if sections:
        result["sections"] = sections

    probes = []
    for spec in args.probe or []:
        pairs = re.findall(r"([xyzXYZ])\s*=\s*(-?[\d.]+)", spec)
        fixed = {"xyz".index(a.lower()): float(v) for a, v in pairs}
        if len(pairs) != 2 or len(fixed) != 2:
            raise ValueError(f"--probe expects two different axes such as z=5,y=40, got {spec!r}")
        stretches, along, odd = probe(verts, faces, fixed)
        probes.append({"line": spec.replace(" ", ""), "along": along, "stretches": stretches,
                       "unreliable": odd})
    if probes:
        result["probes"] = probes

    if preview_path:
        support = []
        for (a, b, c), n in zip(faces, info["normals"]):
            support.append(dot(n, (0, 0, -1)) > OVERHANG_COS
                           and min(verts[a][2], verts[b][2], verts[c][2]) > info["bbox_min"][2] + 0.05)
        bar = preview(preview_path, verts, faces, info["normals"], support, cull=sealed and not info["inverted"])
        result["preview_png"] = preview_path
        result["preview_scale_bar_mm"] = bar

    if args.json:
        return result

    print(f"File: {path}")
    print(f"Size: {size[0]:.1f} x {size[1]:.1f} x {size[2]:.1f} mm   ({len(faces):,} triangles)")
    print(f"Sealed solid: {'yes' if sealed else 'NO'}   Separate pieces: {info['shells']}")
    print(f"Volume: {vol_cm3:.2f} cm3   Surface: {info['area_mm2']:.0f} mm2")
    print(f"Weight in {mat}: {solid_g:.1f} g if solid, about {printed_g:.1f} g printed at {args.infill:g}% infill"
          + (" (thin walls print solid)" if all_solid else ""))
    print()
    print(f"{'Orientation':<20}{'Height mm':>10}{'Bed contact mm2':>17}{'Faces down mm2':>16}")
    for r in table:
        mark = "  <- suggested" if r is best else ""
        print(f"{r['orientation']:<20}{r['height_mm']:>10.1f}{r['bed_contact_mm2']:>17.0f}"
              f"{r['needs_support_mm2']:>16.0f}{mark}")
    print("  (faces down = steeper than 45 degrees above the bed: overhangs that need support,")
    print("   but also short bridges over holes and openings, which print fine up to about 10-15 mm)")
    print()
    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("No warnings.")
    print("Not checked: thin walls and how parts fit. Use --section and --probe on the features that")
    print("must fit, and compare matching parts (e.g. a lid lip against its opening: 0.2-0.3 mm per side).")
    for s in sections:
        lo = s["outlines"]
        print(f"\nSection at {s['plane']} (sizes along {s['axes']}): {len(lo)} outline(s)")
        if not lo:
            print("  nothing here: the plane misses the part")
        for e in lo[:30]:
            dia = f"  round, diameter {e['round_diameter']} mm" if "round_diameter" in e else ""
            if "clear_centre_diameter" in e:
                dia += f"  C-shaped clip or ring: clear diameter {e['clear_centre_diameter']} mm"
            print(f"  {e['kind']:<8} {e['size'][0]:>7.2f} x {e['size'][1]:<7.2f} mm  "
                  f"centre ({e['centre'][0]:.2f}, {e['centre'][1]:.2f}){dia}")
        if len(lo) > 30:
            print(f"  ... {len(lo) - 30} smaller outlines not shown (use --json for all)")
    for p in probes:
        print(f"\nProbe along {p['along']} at {p['line']}:"
              + ("  (odd number of crossings: the mesh isn't sealed here, treat with care)" if p["unreliable"] else ""))
        if not p["stretches"]:
            print("  the line misses the part")
        for st in p["stretches"]:
            print(f"  {st['kind']:<5} {st['from']:>9.2f} -> {st['to']:<9.2f} ({st['length']:.2f} mm)")
    if preview_path:
        print(f"\nPreview: {preview_path}  (left to right: top, front, 3D from above, 3D from below; "
              f"red = faces down as saved; scale bar = {result['preview_scale_bar_mm']:g} mm)")
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("models", nargs="+", help="one or more STL, OBJ or 3MF files (e.g. a case and its lid)")
    ap.add_argument("--material", default="PLA", help="PLA, PETG, ABS, ASA, TPU, NYLON, PA12, RESIN, PC")
    ap.add_argument("--bed", type=parse_dims, help="printer build volume, e.g. 220x220x250")
    ap.add_argument("--infill", type=float, default=20, help="infill percent for the weight estimate")
    ap.add_argument("--preview", help="write a PNG preview here (with several files, one per file)")
    ap.add_argument("--section", action="append", metavar="AXIS=MM",
                    help="cut the part at a height and list the outlines and holes there, "
                         "e.g. z=3 (repeatable). Use it to measure clips, holes and pockets.")
    ap.add_argument("--probe", action="append", metavar="A=MM,B=MM",
                    help="measure along a line, e.g. z=5,y=40 runs along x at z=5, y=40 and lists the "
                         "solid and empty stretches (repeatable). Use it for walls, notches and slots.")
    ap.add_argument("--json", action="store_true", help="print machine-readable JSON")
    args = ap.parse_args()

    results = []
    for i, path in enumerate(args.models):
        pv = args.preview
        if pv and len(args.models) > 1:
            stem, ext = os.path.splitext(pv)
            pv = f"{stem}-{os.path.splitext(os.path.basename(path))[0]}{ext or '.png'}"
        if i and not args.json:
            print("\n" + "=" * 72 + "\n")
        try:
            results.append(check(path, args, pv))
        except (ValueError, OSError, zipfile.BadZipFile, ET.ParseError) as e:
            if args.json:
                results.append({"file": path, "error": str(e)})
            else:
                print(f"File: {path}\n  could not check it: {e}")
    if args.json:
        print(json.dumps(results[0] if len(results) == 1 else results, indent=2))


if __name__ == "__main__":
    main()
