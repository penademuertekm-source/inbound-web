"""Genera la camiseta oversize del prototipo 3D (camiseta.glb) con Blender.

Uso (desde la carpeta prototipo-3d):
  "C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe" --background --factory-startup \
      --python herramientas/generar_camiseta.py -- camiseta.glb

Construye dos piezas, "Frente" y "Espalda", a partir de la silueta de una camiseta oversize
(hombro caído, manga ancha y corta, cuerpo recto). Cada pieza es una malla de cuadrícula con
volumen tipo tela inflada; el borde de ambas coincide (costura lateral) y el frente tiene el
escote abierto. Unidades en metros, eje Y hacia arriba en el GLB.
shortcut: malla procedural sin simulación de tela; sustituir por un modelo de CLO3D/Marvelous
para la versión final.
"""
import bpy, bmesh, math, sys

OUT = sys.argv[sys.argv.index("--") + 1] if "--" in sys.argv else "camiseta.glb"
STEP = 0.009          # tamaño de la cuadrícula (m)
DEPTH = 0.085         # volumen máximo de la tela respecto al plano central (m)
ROLL = 0.11           # distancia al borde en la que la tela "redondea" (m)
NECK_RX, NECK_RY = 0.105, 0.105   # escote delantero (elipse centrada en el cuello)

# Media silueta (x >= 0), de la nuca al bajo, en sentido horario
HALF = [(0.0, -0.022), (0.06, -0.006), (0.105, 0.0), (0.20, -0.026), (0.30, -0.056),
        (0.335, -0.068), (0.42, -0.13), (0.50, -0.205), (0.528, -0.24), (0.47, -0.35),
        (0.44, -0.362), (0.338, -0.282), (0.333, -0.42), (0.336, -0.735), (0.322, -0.75),
        (0.0, -0.752)]
POLY = HALF + [(-x, y) for x, y in reversed(HALF[1:-1])]


def inside(px, py, poly=POLY):
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i], poly[i - 1]
        if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
            c = not c
    return c


def closest_on_poly(px, py, poly=POLY):
    best = (1e9, px, py)
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i - 1], poly[i]
        dx, dy = x2 - x1, y2 - y1
        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        cx, cy = x1 + t * dx, y1 + t * dy
        d = math.hypot(px - cx, py - cy)
        if d < best[0]:
            best = (d, cx, cy)
    return best


def in_neck(px, py):
    return (px / NECK_RX) ** 2 + (py / NECK_RY) ** 2 < 1.0


def neck_closest(px, py):
    a = math.atan2(py / NECK_RY, px / NECK_RX)
    cx, cy = NECK_RX * math.cos(a), NECK_RY * math.sin(a)
    return math.hypot(px - cx, py - cy), cx, cy


def bulge(d):
    t = min(d / ROLL, 1.0)
    return DEPTH * math.sqrt(1.0 - (1.0 - t) ** 2)


def build(name, front):
    sign = 1.0 if front else -1.0
    xs = [round(-0.56 + i * STEP, 5) for i in range(int(1.12 / STEP) + 2)]
    ys = [round(0.02 - j * STEP, 5) for j in range(int(0.80 / STEP) + 2)]
    ok = {(i, j): inside(x, y) and not (front and in_neck(x, y))
          for i, x in enumerate(xs) for j, y in enumerate(ys)}
    bm = bmesh.new()
    verts = {}

    def v(i, j):
        if (i, j) not in verts:
            verts[(i, j)] = bm.verts.new((xs[i], ys[j], 0.0))
        return verts[(i, j)]

    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if ok[(i, j)] and ok[(i + 1, j)] and ok[(i + 1, j + 1)] and ok[(i, j + 1)]:
                # orden de vértices para que la normal apunte hacia fuera (+Z frente, -Z espalda)
                quad = [v(i, j + 1), v(i + 1, j + 1), v(i + 1, j), v(i, j)]
                bm.faces.new(quad if front else list(reversed(quad)))
    bm.verts.ensure_lookup_table()
    boundary = {vv for e in bm.edges if e.is_boundary for vv in e.verts}
    for vv in bm.verts:
        x, y = vv.co.x, vv.co.y
        d, cx, cy = closest_on_poly(x, y)
        if front:
            dn, nx, ny = neck_closest(x, y)
            if dn < d:
                d, cx, cy = dn, nx, ny
        if vv in boundary:
            vv.co.x, vv.co.y, vv.co.z = cx, cy, 0.0   # costura: borde exacto de la silueta
        else:
            vv.co.z = sign * bulge(d)
    # UV planar (la textura cubre la silueta completa)
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for loop in f.loops:
            loop[uv].uv = ((loop.vert.co.x + 0.56) / 1.12, (loop.vert.co.y + 0.78) / 0.80)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    # Blender es Z-arriba: giramos para que el GLB salga con la camiseta de pie (Y-arriba en three.js)
    ob.rotation_euler = (math.radians(90), 0, 0)
    return ob, len(me.polygons)


for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
f_ob, nf = build("Frente", True)
b_ob, nb = build("Espalda", False)
assert nf > 3000 and nb > 3000, (nf, nb)          # autocomprobación: la silueta generó malla
bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.transform_apply(rotation=True)
bpy.ops.export_scene.gltf(filepath=OUT, export_format="GLB", export_yup=True)
print(f"CAMISETA_OK caras frente={nf} espalda={nb} -> {OUT}")
