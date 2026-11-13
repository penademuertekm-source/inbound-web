# INBOUND STUDIO® — web

Web de INBOUND, marca de streetwear *heavyweight oversize* (boxy fit, algodón 310+ GSM).
Página estática en un solo `index.html`, sin dependencias ni paso de compilación.

## Ver la web

Abre `index.html` en el navegador (doble clic). Para probarla en el móvil dentro de la misma red:

```bash
python -m http.server 8080
```

y entra a `http://<IP-de-tu-PC>:8080` desde el teléfono.

## Estructura

```
index.html          Página completa (HTML + CSS + JS en línea)
DESIGN.md           Sistema de diseño: paleta, tipografía, componentes y reglas
assets/             Fotos de la marca, fondo del cierre y logo (logo-inbound.svg)
prototipo-3d/       Prototipo del diseñador 3D (ver abajo)
```

## Prototipo 3D (`prototipo-3d/`)

Demostración funcional de la idea de la marca: el cliente coloca gráficos de INBOUND, su frase o su
propia imagen sobre una camiseta en 3D, en móvil y en PC. Se abre con doble clic en `prototipo-3d/index.html`.

- **Prenda:** corte Oversize / Boxy fit y los 4 colores de la guía de identidad.
- **Diseño:** gráficos de la marca, frase propia e imagen subida; se arrastran sobre la tela, con tamaño y rotación.
- **Validación:** área imprimible, resolución de imágenes (150 ppp mínimo), contraste con la prenda y técnica (serigrafía, DTF o alta densidad).
- **Exportar:** descarga una imagen PNG del diseño.

Tecnología: [three.js](https://threejs.org) 0.186.1 (MIT) desde CDN, sin compilación.
El modelo `camiseta.glb` lo genera `herramientas/generar_camiseta.py` con Blender 5
(`camiseta-glb.js` es el mismo modelo empaquetado para poder abrir la página sin servidor).

**Limitaciones del prototipo:** la camiseta es una malla procedural (sin pliegues reales); para la versión final
hay que modelarla en CLO3D o Marvelous Designer con los patrones de INBOUND. Aún no hay paso de IA ni pedido online.

## Secciones

1. **Hero:** Heavyweight Oversize Culture.
2. **Diseña tu INBOUND:** configurador (corte, color, gramaje, gráfico, frase, talla) con vista previa, tinta y técnica automáticas. El pedido se copia y se envía por Instagram.
3. **Drop 001:** prendas en stock.
4. **Del diseño a la prenda:** los 7 pasos del proceso.
5. **Cómo se imprime una INBOUND:** serigrafía, DTF, alta densidad y el taller.
6. **Tu estilo, nuestra esencia:** las tres líneas.
7. **Cierre:** réplica de la página 10 del PDF de marca.

## Tipografías

- [Archivo](https://fonts.google.com/specimen/Archivo) y [Montserrat](https://fonts.google.com/specimen/Montserrat), cargadas desde Google Fonts (licencia SIL OFL).

## Pendiente

- Precios del Drop 001 (por ahora los pedidos van por Instagram).
- Logo oficial en vector (el actual está redibujado a partir del PDF).
- Año de fundación: la foto del hero dice 2024 y la web 2025.
- Modelo 3D realista de la camiseta (CLO3D / Marvelous) y paso de visualización con IA.

## Derechos

La marca INBOUND, el logo y todas las imágenes de `assets/` son © INBOUND STUDIO.
Este repositorio es público solo para consulta: no se concede licencia para reutilizar la marca ni las imágenes.
