"""Prepara los modelos de los cortes del estudio 3D a partir de los FBX de CGTrader (exportados desde CLO3D).

Modelos (fashion3designn, CGTrader, Royalty Free License (no AI): uso personal y comercial):
  Normal   -> "Male regular fit tshirt"  https://www.cgtrader.com/free-3d-models/character/clothing/male-regular-fit-tshirt
  Boxy fit -> "Male oversized tshirt"    https://www.cgtrader.com/free-3d-models/character/clothing/male-oversized-tshirt
  Oversize -> la Boxy fit alargada aquí (cuerpo por debajo de la sisa y mangas), como modelo propio

Uso (desde prototipo-3d; los FBX son ASCII y solo los lee el importador nuevo de Blender 5, wm.fbx_import):
  blender --background --factory-startup --python herramientas/preparar_camisetas_cgtrader.py -- <origen.fbx> <salida.glb> [alargar]

Pasos: separa las piezas sueltas, descarta pespuntes y vistas internas (piezas de menos de 4 cm²), de cada pieza
doble de CLO (cara exterior + cara interior de la tela) conserva la exterior, clasifica Frente / Espalda / Mangas /
Cuello, centra la prenda (punto más alto del cuello en z=0, frente hacia -Y = +Z en el GLB), opcionalmente la
alarga (Oversize) y reduce polígonos a un tamaño apto para móvil.
"""
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix

ARGS = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = ARGS[:2]
ALARGAR = len(ARGS) > 2 and ARGS[2] == "alargar"
TARGET = {"Frente": 9000, "Espalda": 9000, "Mangas": 5000, "Cuello": 1500}   # caras finales por pieza (~25k en total)
MIN_AREA = 4e-4                                                              # 4 cm²: por debajo son pespuntes o vistas

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.fbx_import(filepath=SRC)
src = [o for o in bpy.context.scene.objects if o.type == "MESH"]
assert len(src) == 1, "se esperaba una sola malla (exportación de CLO)"
ob = src[0]
ob.data.transform(ob.matrix_world); ob.matrix_world = Matrix.Identity(4)   # todo en metros, en coordenadas de mundo
for o in [o for o in bpy.context.scene.objects if o.type != "MESH"]:
    bpy.data.objects.remove(o, do_unlink=True)

bpy.context.view_layer.objects.active = ob; ob.select_set(True)
bpy.ops.object.mode_set(mode="EDIT"); bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.mesh.separate(type="LOOSE"); bpy.ops.object.mode_set(mode="OBJECT")
parts = [o for o in bpy.context.scene.objects if o.type == "MESH"]


def info(o):
    vs = [v.co for v in o.data.vertices]
    c = sum(vs, Vector()) / len(vs)
    area = sum(p.area for p in o.data.polygons)
    return c, area, vs


# Cuerpo: las dos piezas más grandes (cada una con su doble) son frente y espalda
meta = {o: info(o) for o in parts}
big = sorted(parts, key=lambda o: -meta[o][1])[:4]
cx = sum(meta[o][0].x for o in big) / 4
cy = sum(meta[o][0].y for o in big) / 4
top = max(v.z for o in parts for v in meta[o][2])
body_x = max(abs(v.x - cx) for o in big for v in meta[o][2])


def classify(o):
    c, area, vs = meta[o]
    if area < MIN_AREA:
        return None
    # cinta interior del cuello trasero ("... Copy ..." en CLO): va por dentro y, con menos polígonos, atravesaba la
    # espalda y se veía como una mancha clara bajo el cuello
    if any("Copy" in (o.data.materials[p.material_index].name if o.data.materials else "") for p in o.data.polygons[:50]):
        return None
    if o in big:
        return "Frente" if c.y < cy else "Espalda"
    if c.z > top - 0.12 and abs(c.x - cx) < 0.13:
        return "Cuello"
    if abs(c.x - cx) > body_x * 0.62:
        return "Mangas"
    return None   # vistas, refuerzos interiores, bandas del bajo


groups = {}
for o in parts:
    g = classify(o)
    if g:
        groups.setdefault(g, []).append(o)
    else:
        bpy.data.objects.remove(o, do_unlink=True)


def radial(o):
    vs = meta[o][2]
    return sum(math.hypot(v.x - cx, v.y - cy) for v in vs) / len(vs)


# De cada pareja de CLO (misma pieza, dos caras de la tela separadas ~1 mm) se queda la más exterior
keep = {}
for g, objs in groups.items():
    if g == "Cuello":
        for o in objs:
            keep[o] = g
        continue
    objs = sorted(objs, key=lambda o: -len(o.data.polygons))
    used = set()
    for o in objs:
        if o in used:
            continue
        twin = [p for p in objs if p not in used and p is not o and abs(len(p.data.polygons) - len(o.data.polygons)) <= 2
                and (meta[p][0] - meta[o][0]).length < 0.01]
        cand = [o] + twin[:1]
        used.update(cand)
        best = max(cand, key=radial)
        keep[best] = g
for o in [o for o in bpy.context.scene.objects if o.type == "MESH" and o not in keep]:
    bpy.data.objects.remove(o, do_unlink=True)

# Centrar: x / profundidad en el centro del cuerpo; punto más alto en z = 0
shift = Matrix.Translation((-cx, -cy, -top))
for o in keep:
    o.data.transform(shift)

# Unir por pieza, alargar (Oversize), reducir y suavizar
mat = bpy.data.materials.new("Tela")
final = {}
for name in ("Frente", "Espalda", "Mangas", "Cuello"):
    objs = [o for o, n in keep.items() if n == name]
    assert objs, f"falta la pieza {name}"
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    m = bpy.context.view_layer.objects.active
    m.name = m.data.name = name
    final[name] = m

if ALARGAR:
    # Oversize: el cuerpo crece ~10 cm desde 3 cm por DEBAJO de la axila y las mangas ~25 % hacia el puño.
    # Antes el estiramiento empezaba 2 cm por encima del punto más bajo de la sisa: el cuerpo bajaba hasta 7 mm junto a la
    # axila y se abría un hueco entre cuerpo y manga. Ahora la sisa entera y todo lo de arriba quedan quietos.
    sisa = min(v.co.z for v in final["Mangas"].data.vertices) - 0.03
    bajo = min(v.co.z for n in ("Frente", "Espalda") for v in final[n].data.vertices)
    k = (sisa - bajo + 0.10) / (sisa - bajo)
    for n in ("Frente", "Espalda"):
        for v in final[n].data.vertices:
            if v.co.z < sisa:
                v.co.z = sisa - (sisa - v.co.z) * k
    # Mangas: la costura de la sisa (vértices a menos de 1,5 cm del cuerpo) queda fija; solo se alarga lo que está
    # más allá de su punto más lejano sobre el eje de la manga. Así la manga no se despega del hombro
    from mathutils.kdtree import KDTree
    body_pts = [v.co.copy() for n in ("Frente", "Espalda") for v in final[n].data.vertices]
    kd = KDTree(len(body_pts))
    for i, p in enumerate(body_pts):
        kd.insert(p, i)
    kd.balance()
    for side in (1, -1):
        vs = [v for v in final["Mangas"].data.vertices if v.co.x * side > 0]
        pts = [v.co for v in vs]
        c = sum(pts, Vector()) / len(pts)
        seam = [p for p in pts if kd.find(p)[2] < 0.015]
        s0 = sum(seam, Vector()) / len(seam)
        axis = (c - s0).normalized()
        t0 = max((p - s0).dot(axis) for p in seam)
        for v in vs:
            t = (v.co - s0).dot(axis) - t0
            if t > 0:
                v.co += axis * t * 0.25
    print(f"CAMISETA alargada: k_cuerpo={k:.2f} sisa_z={sisa:.3f}")

# Reducir polígonos pieza por pieza. (Probado: soldar las costuras y reducir todo junto dejaba dientes en los puños
# y no cerraba más las costuras, porque CLO deja las piezas solapadas unos milímetros.)
for name, m in final.items():
    ratio = min(1.0, TARGET[name] / max(1, len(m.data.polygons)))
    if ratio < 1:
        dec = m.modifiers.new("reducir", "DECIMATE"); dec.ratio = ratio
        bpy.context.view_layer.objects.active = m
        bpy.ops.object.modifier_apply(modifier=dec.name)
    m.data.materials.clear(); m.data.materials.append(mat)
    for p in m.data.polygons:
        p.use_smooth = True

# Alisar pliegues: al reducir polígonos, algún triángulo puede quedar dado la vuelta (normal a más de 110° de las
# de sus vecinos). En la Normal pasaba en la espalda bajo el cuello y se veía como una mancha clara. Se relajan esos
# vértices y su entorno (sin tocar bordes) hasta que no quede ninguno. Solo en Frente y Espalda: en mangas y cuello hay
# dobleces reales (puño vuelto, ribete) que tienen ángulos así a propósito y no se deben alisar
import math as _m
for name in ("Frente", "Espalda"):
    m = final[name]
    bm = bmesh.new(); bm.from_mesh(m.data)
    for ronda in range(12):
        bm.normal_update()
        bad = set()
        for f in bm.faces:
            nb = [g for e in f.edges for g in e.link_faces if g is not f]
            if nb:
                avg = sum((g.normal for g in nb), Vector())
                if avg.length > 1e-9 and _m.degrees(f.normal.angle(avg, 0)) > 110:
                    bad.update(f.verts)
        if not bad:
            break
        ring = set(bad)
        for v in bad:
            for e in v.link_edges:
                ring.add(e.other_vert(v))
        movable = [v for v in ring if not any(e.is_boundary for e in v.link_edges)]
        bmesh.ops.smooth_vert(bm, verts=movable, factor=0.6, use_axis_x=True, use_axis_y=True, use_axis_z=True)
    print(f"CAMISETA pliegues {name}: {len(bad)} vértices sin resolver tras {ronda + 1} rondas")
    bm.to_mesh(m.data); bm.free()

# Cerrar costuras: cada vértice de borde que queda a menos de 8 mm de otra pieza se pega a su superficie.
# CLO deja rendijas pequeñas entre piezas (y la reducción de polígonos las agranda); en la costura lateral del bajo o
# junto al cuello se veía el fondo. Los bordes que de verdad son aberturas (bajo, puños, cuello) quedan más lejos y no se tocan
from mathutils.bvhtree import BVHTree
CIERRE = 0.008
for name, m in final.items():
    others = [o for n, o in final.items() if n != name]
    verts, polys, off = [], [], 0
    for o in others:
        verts += [v.co.copy() for v in o.data.vertices]
        polys += [[i + off for i in poly.vertices] for poly in o.data.polygons]
        off += len(o.data.vertices)
    tree = BVHTree.FromPolygons(verts, polys)
    bm = bmesh.new(); bm.from_mesh(m.data)
    moved = 0
    for v in bm.verts:
        if any(e.is_boundary for e in v.link_edges):
            hit = tree.find_nearest(v.co)
            if hit[0] is not None and hit[3] < CIERRE:
                v.co = hit[0]; moved += 1
    bm.to_mesh(m.data); bm.free()
    print(f"CAMISETA costura {name}: {moved} vértices pegados")

# Todas las piezas con la cara exterior hacia fuera (el estudio pinta el interior más oscuro con BackSide).
# Por cada isla (cada manga, cada capa del cuello…): orientación coherente y, si la mayoría de su área mira hacia el
# eje vertical del cuerpo, se invierte
def radial_out(f):
    c = f.calc_center_median(); r = Vector((c.x, c.y, 0))
    return f.normal.dot(r.normalized()) * f.calc_area() if r.length > 1e-4 else 0.0


for name, m in final.items():
    bm = bmesh.new(); bm.from_mesh(m.data)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    seen = set()
    for f0 in bm.faces:
        if f0.index in seen:
            continue
        isle, stack = [], [f0]
        seen.add(f0.index)
        while stack:
            f = stack.pop(); isle.append(f)
            for e in f.edges:
                for g in e.link_faces:
                    if g.index not in seen:
                        seen.add(g.index); stack.append(g)
        if sum(radial_out(f) for f in isle) < 0:
            bmesh.ops.reverse_faces(bm, faces=isle)
    bm.to_mesh(m.data); bm.free()

# Normales hacia fuera: frente hacia -Y, espalda hacia +Y (en Blender)
for name, sign in (("Frente", -1), ("Espalda", 1)):
    m = final[name]
    n = sum((p.normal * p.area for p in m.data.polygons), Vector())
    if n.y * sign < 0:
        bm = bmesh.new(); bm.from_mesh(m.data)
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(m.data); bm.free()

faces = {n: len(m.data.polygons) for n, m in final.items()}
fy = sum(v.co.y for v in final["Frente"].data.vertices) / len(final["Frente"].data.vertices)
by = sum(v.co.y for v in final["Espalda"].data.vertices) / len(final["Espalda"].data.vertices)
assert fy < by, "el frente debería quedar delante (-Y)"
assert sum(faces.values()) < 40000, faces

bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_yup=True)
fx = [v.co.x for v in final["Frente"].data.vertices]; fz = [v.co.z for v in final["Frente"].data.vertices]
print(f"CAMISETA_OK caras={faces} frente_x=[{min(fx):.3f},{max(fx):.3f}] alto=[{min(fz):.3f},{max(fz):.3f}] -> {OUT}")
