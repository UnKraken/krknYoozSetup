# Manual de instalación Yooz2SageNG v1.2

Versión editable reconstruida a partir del PDF facilitado. Conserva el idioma, el contenido técnico, las 13 páginas, las capturas, los colores, las cabeceras y la distribución del original. No se ha actualizado todavía la información técnica ni el número de versión impreso.

## Abrir y editar

1. Descarga `docs/Manual_de_instalacion_Yooz2SageNG_v1.2.html` y ábrelo con Chrome, Edge o Firefox.
2. Haz clic sobre el texto que quieras cambiar.
3. Pulsa **Guardar cambios** para descargar el HTML actualizado. El navegador no modifica el archivo original ni lo sube a GitHub.
4. Sustituye el archivo del repositorio por el HTML actualizado para conservar la revisión.

Las imágenes y las fuentes están incluidas en el HTML; funciona sin conexión y no carga recursos externos. Las capturas conservan su condición de imágenes. Los textos del documento se pueden editar y seleccionar.

Se mantiene una maquetación fija por páginas para reproducir el original. Los textos largos, nuevas secciones, filas o capturas requieren ajustar las posiciones o añadir páginas. El contenido de las capturas no es texto editable. Para cambios extensos, pide la actualización del documento y su maquetación conjuntamente.

## Generar PDF

Para una exportación rápida, pulsa **Generar PDF** y elige Guardar como PDF en el navegador, sin márgenes ni cabeceras del navegador y con los gráficos de fondo activados.

Para una generación reproducible con las coordenadas y fuentes del documento:

```sh
python -m pip install -r requirements.txt
python scripts/generar_pdf.py
```

El resultado se guarda en `dist/Manual_de_instalacion_Yooz2SageNG_v1.2.pdf`.

El generador usa el HTML como única fuente del texto. No necesita el PDF original ni un navegador. Conserva las imágenes, las fuentes incrustadas y los enlaces del original.

También está disponible el flujo **Generar PDF del manual** en la pestaña Actions. Genera un PDF descargable como artefacto al actualizar el manual en `main` o al ejecutarlo manualmente. El artefacto queda sujeto al periodo de retención de GitHub Actions; el HTML es la fuente permanente.

## Archivos

- `docs/Manual_de_instalacion_Yooz2SageNG_v1.2.html`: documento fuente editable y autónomo.
- `scripts/generar_pdf.py`: generador de PDF.
- `requirements.txt`: dependencia del generador.
- `.github/workflows/manual-pdf.yml`: generación del PDF en GitHub Actions.
