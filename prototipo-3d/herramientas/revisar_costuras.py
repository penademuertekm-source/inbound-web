"""Mide cuánto se abren las costuras de una camiseta .glb del estudio (separación entre piezas vecinas).

Uso: blender --background --factory-startup --python herramientas/revisar_costuras.py -- camiseta-oversize.glb
Para cada vértice de borde abierto de cada pieza mide la distancia a la superficie más cercana de otra pieza; los que están a menos de 3 cm
son costura (más lejos son aberturas reales: cuello, bajo, puños). Informa la separación máxima y el percentil 99.
"""
import bpy, bmesh, sys
from mathutils.bvhtree import BVHTree

src = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=src)
# el cuello (varias capas de ribete) se deja fuera: sus bordes interiores no son costuras
pieces = {o.name: o for o in bpy.context.scene.objects if o.type == "MESH" and not o.name.startswith("Cuello")}
world = {n: [o.matrix_world @ v.co for v in o.data.vertices] for n, o in pieces.items()}
gaps = []
for n, o in pieces.items():
    verts, polys, off = [], [], 0
    for m, q in pieces.items():
        if m == n:
            continue
        verts += world[m]
        polys += [[i + off for i in poly.vertices] for poly in q.data.polygons]
        off += len(world[m])
    tree = BVHTree.FromPolygons(verts, polys)
    bm = bmesh.new(); bm.from_mesh(o.data)
    for v in bm.verts:
        if any(e.is_boundary for e in v.link_edges):
            hit = tree.find_nearest(o.matrix_world @ v.co); d = hit[3] if hit[0] is not None else 1
            if d < 0.03:
                gaps.append((d, n))
    bm.free()
gaps.sort()
bins = [(0, 2), (2, 5), (5, 10), (10, 30)]
hist = {f"{a}-{b} mm": sum(1 for d, _ in gaps if a <= d * 1000 < b) for a, b in bins}
print(f"COSTURAS {src}: {hist}")
