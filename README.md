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
```

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
- Prototipo de configurador 3D (three.js) para colocar diseños sobre la camiseta.

## Derechos

La marca INBOUND, el logo y todas las imágenes de `assets/` son © INBOUND STUDIO.
Este repositorio es público solo para consulta: no se concede licencia para reutilizar la marca ni las imágenes.
