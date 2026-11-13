"""Prepara la camiseta de Sketchfab para el prototipo (camiseta.glb).

Modelo: "T Shirt" de funlab117, licencia CC BY 4.0 (uso comercial permitido citando al autor)
https://sketchfab.com/3d-models/t-shirt-c1a3e5eb9b5445f4b7d4be82f1127eba

Uso (desde prototipo-3d):
  "C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe" --background --factory-startup \
      --python herramientas/preparar_camiseta_sketchfab.py -- <ruta>/t_shirt.glb camiseta.glb

Pasos: quita las capas interiores de tela, endereza la prenda (frente hacia +Z en el GLB),
la centra con el punto más alto del cuello en y=0, reduce polígonos y exporta las piezas
Frente / Espalda (reciben diseños) y Mangas / Cuello (solo visuales).
"""
import bpy, bmesh, math, sys
from mathutils import Vector, Matrix

SRC, OUT = sys.argv[sys.argv.index("--") + 1:][:2]
RATIO = 0.42          # proporción de caras que se conservan al reducir

for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
bpy.ops.import_scene.gltf(filepath=SRC)
bpy.context.view_layer.update()


def group(o):
    p = o
    while p:
        for key in ("Body_Front", "Body_Back", "Sleeves", "Ribbing"):
            if key in p.name:
                return key
        p = p.parent
    return None


def world_verts(o):
    return [o.matrix_world @ v.co for v in o.data.vertices]


def centroid(objs):
    pts = [v for o in objs for v in world_verts(o)]
    return sum(pts, Vector()) / len(pts)


meshes = [o for o in bpy.data.objects if o.type == "MESH"]
groups = {k: [o for o in meshes if group(o) == k] for k in ("Body_Front", "Body_Back", "Sleeves", "Ribbing")}
assert groups["Body_Front"] and groups["Body_Back"], "no se encontraron las piezas del cuerpo"
center = centroid(groups["Body_Front"] + groups["Body_Back"])


def outer_layer(objs):
    # de las dos capas grandes de tela, la exterior es la más alejada del centro del cuerpo
    big = sorted(objs, key=lambda o: -len(o.data.polygons))[:2]
    dist = lambda o: sum(((v - center) * Vector((1, 1, 0))).length for v in world_verts(o)) / len(o.data.vertices)
    return max(big, key=dist)


front, back = outer_layer(groups["Body_Front"]), outer_layer(groups["Body_Back"])
keep = {front: "Frente", back: "Espalda"}
for o in groups["Sleeves"]:
    keep[o] = "Mangas"
for o in groups["Ribbing"]:
    keep[o] = "Cuello"
for o in meshes:
    if o not in keep:
        bpy.data.objects.remove(o, do_unlink=True)

# Hornear transformaciones y quitar jerarquía
for o in list(keep):
    mw = o.matrix_world.copy()
    o.parent = None
    o.data.transform(mw)
    o.matrix_world = Matrix.Identity(4)
for o in [o for o in bpy.data.objects if o.type == "EMPTY"]:
    bpy.data.objects.remove(o, do_unlink=True)

# Enderezar: el eje principal en planta (hombro a hombro, mangas incluidas) pasa a ser X;
# luego, si el frente no queda en -Y (frente en Blender = +Z en el GLB), se gira 180°
pts = [v.co for o in keep for v in o.data.vertices]
mx, my = sum(p.x for p in pts) / len(pts), sum(p.y for p in pts) / len(pts)
sxx = sum((p.x - mx) ** 2 for p in pts); syy = sum((p.y - my) ** 2 for p in pts)
sxy = sum((p.x - mx) * (p.y - my) for p in pts)
theta = 0.5 * math.atan2(2 * sxy, sxx - syy)
for o in keep:
    o.data.transform(Matrix.Rotation(-theta, 4, "Z"))
if centroid([front]).y > centroid([back]).y:
    for o in keep:
        o.data.transform(Matrix.Rotation(math.pi, 4, "Z"))

# Centrar: x y profundidad en el centro del cuerpo; punto más alto en z=0
body = [v for o in (front, back) for v in (x.co for x in o.data.vertices)]
allv = [v.co for o in keep for v in o.data.vertices]
cx = (min(v.x for v in body) + max(v.x for v in body)) / 2
cy = (min(v.y for v in body) + max(v.y for v in body)) / 2
top = max(v.z for v in allv)
shift = Matrix.Translation((-cx, -cy, -top))
for o in keep:
    o.data.transform(shift)

# Unir por pieza, reducir polígonos, un solo material y sombreado suave
mat = bpy.data.materials.new("Tela")
final = {}
for name in ("Frente", "Espalda", "Mangas", "Cuello"):
    objs = [o for o, n in keep.items() if n == name]
    if not objs:
        continue
    bpy.ops.object.select_all(action="DESELECT")
    for o in objs:
        o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]
    if len(objs) > 1:
        bpy.ops.object.join()
    ob = bpy.context.view_layer.objects.active
    ob.name = ob.data.name = name
    if name != "Cuello":
        dec = ob.modifiers.new("reducir", "DECIMATE")
        dec.ratio = RATIO
        bpy.ops.object.modifier_apply(modifier=dec.name)
    ob.data.materials.clear()
    ob.data.materials.append(mat)
    for p in ob.data.polygons:
        p.use_smooth = True
    final[name] = ob

# Frente: las normales deben mirar hacia fuera (-Y en Blender); si no, se invierten
for name, sign in (("Frente", -1), ("Espalda", 1)):
    ob = final[name]
    n = sum((p.normal for p in ob.data.polygons), Vector())
    if n.y * sign < 0:
        bm = bmesh.new(); bm.from_mesh(ob.data)
        bmesh.ops.reverse_faces(bm, faces=bm.faces)
        bm.to_mesh(ob.data); bm.free()

faces = {n: len(o.data.polygons) for n, o in final.items()}
fz = sum(v.co.y for v in final["Frente"].data.vertices) / len(final["Frente"].data.vertices)
bz = sum(v.co.y for v in final["Espalda"].data.vertices) / len(final["Espalda"].data.vertices)
assert fz < bz, "el frente debería quedar delante (-Y)"            # autocomprobación de orientación
assert sum(faces.values()) < 90000, faces                            # tamaño apto para móvil

bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_yup=True)
xs = [v.co.x for v in final["Frente"].data.vertices]; zs = [v.co.z for v in final["Frente"].data.vertices]
print(f"CAMISETA_OK caras={faces} frente_x=[{min(xs):.3f},{max(xs):.3f}] alto=[{min(zs):.3f},{max(zs):.3f}] -> {OUT}")
