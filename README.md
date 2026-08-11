# Maquitos — Import Profit Lab

Simulador web para proyectar la rentabilidad de importaciones desde China hacia Perú antes de comprometer capital.

## App

**URL prevista en GitHub Pages:** https://mjm03.github.io/maquitos/

> Si el enlace todavía no carga, en el repositorio entra a **Settings → Pages → Build and deployment → Source: GitHub Actions**. El workflow incluido en este repo publicará el sitio automáticamente.

## Qué calcula

- FOB, valor aduanero aproximado y costos logísticos.
- Ad valorem configurable.
- IGV + IPM, ISC y derechos adicionales configurables.
- Percepción del IGV separada como salida de caja para evitar confundirla automáticamente con costo económico definitivo.
- Costo puesto por unidad y caja total requerida.
- Unidades vendibles considerando merma.
- Utilidad proyectada, ROI económico y margen neto.
- Punto de equilibrio.
- Precio objetivo para distintos márgenes.
- Sensibilidad ante cambios de precio, flete y tipo de cambio.
- Comparación con precio local de referencia.
- Alertas sobre subpartida, flete alto, rentabilidad débil y posibles restricciones.
- Guardado local de escenarios, copia de resumen, exportación CSV e impresión/PDF.

## Importa Fácil

La app incluye una aproximación para envíos postales: FOB hasta US$200 se proyecta sin ad valorem ni IGV cuando aplica; entre US$200 y US$2,000 se usa como referencia la partida única de 4% de ad valorem + 18% de IGV. Siempre deben revisarse exclusiones, mercancías restringidas y el tratamiento real determinado por SUNAT.

## Aviso

Maquitos es una herramienta de proyección y no reemplaza una liquidación aduanera oficial. Aranceles, restricciones, medidas antidumping, ISC, percepción, valoración aduanera, TLC/origen y gastos logísticos pueden variar por producto y operación.

Fuentes de referencia: SUNAT — Importación, Tributos a cancelar e Importa Fácil.