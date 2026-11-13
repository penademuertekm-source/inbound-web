# INBOUND STUDIO® — Design Language

Fuentes: "Identidad_visual_INBOUND.pdf" (guía oficial: paleta, botones, fondos) + "Black and White Modern Fashion
Brand Strategy Presentation.pdf" (10 páginas: contenido, fotos, proceso) + bio de Instagram @inbound.st
("Heavyweight Oversize Culture. Boxy Fit / 310+ GSM Cotton. Drop 001. Stock limitado.").
Valores marcados *(provisional)* no vienen del PDF: los decidí yo y deben confirmarse.

## Visual Theme
**Pesado, nocturno, industrial — streetwear de taller.**
Blanco y negro con fotografía oscura de producto y de taller (serigrafía, DTF, prensa, empaque). La marca se
muestra como un estudio que fabrica, no como una tienda genérica. Referencias del PDF: titulares extendidos
y muy pesados ("CÓMO FUNCIONA?", "CUELLO DE BOTELLA", "MERCADO"), wordmark condensado en portada,
botones píldora, hairlines finas, moodboard con 4 swatches.

Idea rectora: **el peso es la marca** (310+ GSM). La tipografía lo expresa con el eje de anchura de una sola
familia: condensada en etiquetas, expandida y negra en titulares.

## Color Palette
Fuente oficial: `Identidad_visual_INBOUND.pdf` (manda sobre los swatches del moodboard). Fondos principalmente
blanco y negro; sin acentos saturados, el color lo pone la fotografía.

| Token | Valor | Rol |
|-------|-------|-----|
| `ink` | `#080808` | Color principal: fondos oscuros, botones y texto sobre blanco |
| `white` | `#FFFFFF` | Contraste y fondos claros |
| `gray` | `#858585` | Textos secundarios sobre negro (5.2:1) |
| `beige` | `#D6D0C5` | Detalles cálidos (indicador de stock) |
| `gray-text` | `#6E6E6E` | Derivado: texto secundario sobre blanco. `#858585` sobre blanco da 3.7:1 y no pasa AA *(provisional)* |
| `tint` | `#EEEBE6` | Derivado: beige al 45% sobre blanco, fondo de la vista previa y del campo de texto *(provisional)* |
| `line-dark` / `line-light` | `rgba(0,0,0,.18)` / `rgba(255,255,255,.22)` | Hairlines |

Colores de prenda del configurador = los cuatro de la paleta (negro, blanco, gris, beige).

Estados (guía: "estados suaves"): botón sólido hover = opacidad 0.8; botón contorno hover = velo gris 20%;
seleccionado = fondo `ink`, texto `white`; foco = contorno 2px `ink` sobre claro, `white` sobre negro, offset 3px.
Botones: negros con texto blanco; sobre fondo negro se usa la versión invertida (blanco con texto negro).

## Typography
**Familia única:** Archivo (Google Fonts, variable `wdth 62–125`, `wght 100–900`) — fallback `"Arial Narrow", Arial, sans-serif`.

| Rol | Ajuste | Uso |
|-----|--------|-----|
| Display | `wdth 125`, `wght 850–900`, mayúsculas, tracking -0.02em, lh 0.88 | Wordmark del hero, titulares de sección |
| Etiqueta | `wdth 72`, `wght 600`, tracking +0.02em, sentence case | Nav, specs, etiquetas de controles |
| Cuerpo | `wdth 100`, `wght 400`, lh 1.55, medida ≤ 62ch | Párrafos |

**Cierre (réplica de la pág. 10 del PDF):** Montserrat 500/600 (Google Fonts) para lema, botón "Compra ahora" y
pie, en mayúsculas con tracking amplio (.12em botón, .36em lema). Logo: `assets/logo-inbound.svg`, wordmark
redibujado del PDF (no hay archivo vectorial oficial). Fuentes embebidas en el PDF de estrategia: Monument Extended
Bold (titulares pág. 7–9), Oswald Bold, Quicksand, Glacial Indifference, DM Sans, Prompt, Open Sauce One.

Escala modular 1.333 (expresiva), base 16px:

| Token | px | rem | Rol |
|-------|----|-----|-----|
| `xs` | 12 | 0.75 | Pie, notas |
| `sm` | 14 | 0.875 | Etiquetas |
| `base` | 16 | 1 | Cuerpo |
| `md` | 21 | 1.333 | Entradilla |
| `lg` | 28 | 1.777 | Títulos de tarjeta / paso |
| `xl` | 38 | 2.369 | H2 móvil |
| `2xl` | 50–96 (clamp) | — | H2 escritorio |
| `display` | clamp(64px, 17vw, 300px) | — | Wordmark hero |

## Components
| Componente | Nivel | Propósito | Variantes |
|-----------|-------|-----------|-----------|
| Botón píldora | Primitivo | Acción principal / secundaria | sólido (ink o bone), contorno |
| Chip de opción | Primitivo | Elegir corte, gramaje, gráfico, talla | por defecto, seleccionado (`ink`), foco |
| Swatch | Primitivo | Elegir color de prenda | 5 colores, seleccionado con anillo |
| Header | Componente | Wordmark + nav de anclas + Instagram | claro sobre negro |
| Ficha de producto | Componente | Prenda del Drop 001 | grande (destacada), estándar |
| Paso de proceso | Componente | Una etapa de "Del diseño a la prenda" (secuencia real: numerada) | 7 pasos |
| Técnica | Componente | Serigrafía / DTF / Alta densidad con foto | 3 |
| Configurador | Patrón | Diseña tu INBOUND: vista previa SVG + controles + validación + resumen | — |

## Layout
**Grid:** fluido de 12 columnas, márgenes `clamp(16px, 4vw, 56px)`, gutter 24px.
**Base:** 8px. Escala: xs 4 · sm 8 · md 16 · lg 24 · xl 32 · 2xl 48 · 3xl 64 · 4xl 96 · 5xl 144.
Alineación a la izquierda. Secciones alternan negro / hueso. Radio: 999px solo en botones píldora y chips; 0 en
fotos y paneles (fotografía a sangre, como el PDF).

## Depth
Plano. Sin sombras. La jerarquía se construye con contraste negro/hueso, tamaño y hairlines.

## Do's and Don'ts
### Do
- Usar las fotos reales de la marca (taller, prendas, empaque) a sangre y en escala de grises/oscuras.
- Expresar jerarquía con el eje de anchura de Archivo, no con más familias.
- Numerar solo lo que es secuencia (los 7 pasos del proceso).
- Usar el beige solo como detalle cálido, nunca como fondo de sección.
- Escribir en español, frases cortas, verbos claros ("Diseña tu camiseta", "Copiar pedido").

### Don't
- No añadir colores saturados ni degradados decorativos.
- No usar sombras ni tarjetas redondeadas idénticas.
- No usar etiquetas en mayúsculas espaciadas encima de cada título.
- No animar cada sección: un solo momento de movimiento (el wordmark del hero se expande al cargar).
- No inventar precios: el pedido se cierra por Instagram hasta que exista checkout.

## Responsive
Mobile-first. `< 768px`: una columna; nav como fila desplazable; configurador apila vista previa sobre controles.
`≥ 1024px`: la vista previa queda fija (sticky) mientras se recorren los controles. `≥ 1024px`: configurador en dos columnas, Drop 001 en mosaico asimétrico.
Proceso: fila con scroll-snap horizontal en todos los anchos.

## Agent Prompt Guide
- Una sola familia (Archivo); el contraste viene de `wdth` y `wght`.
- Paleta cerrada de la guía: ink #080808, white #FFFFFF, gray #858585, beige #D6D0C5 (+ derivados gray-text y tint).
- Lema de marca: "Own your style".
- Base 8px; radio solo 0 o píldora.
- Un único movimiento automático (hero); respetar `prefers-reduced-motion`.
- Contenido real del PDF; todo lo inventado se marca como provisional.
