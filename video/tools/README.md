# Herramientas del logo

Scripts recuperados del proyecto local y adaptados para trabajar dentro del repositorio. Los archivos originales del proyecto padre se conservan.

## Requisitos
Python, NumPy y Pillow. El render requiere además FFmpeg con codificador libx264 disponible en PATH. No se instalan automáticamente.

## Render de la animación
Desde la raíz del repositorio:

```sh
python video/tools/render_voxwave.py
```

Lee la fuente de animación histórica de video/assets/logo/VoxWave-vector/VoxWave-animation-source.svg y genera MP4, GIF, storyboard, fotograma final y verification.json en video/renders/drafts/logo-reveal. Estos resultados están excluidos de Git. Volver a ejecutar sustituye los resultados de esa carpeta, sin modificar el logo oficial ni los demás assets incorporados.

## Vectorización
```sh
python video/tools/vectorize_voxwave.py /ruta/al/logo-original.png
```

Genera dos SVG con nombres `VoxWave-generated-*` en video/renders/drafts/vectorized-logo. Puede elegirse otro destino mediante --output-dir. Está diseñado para la composición y paleta del logo original, no para imágenes arbitrarias; no sobrescribe los SVG oficiales.

El script original dependía de un PNG en una carpeta temporal de Windows. Ese archivo no forma parte del material encontrado; ahora se proporciona explícitamente como entrada. La vista previa incluida no se presenta como sustituto exacto del original.

## Verificación de incorporación
Se comprueba la integridad de las copias y la sintaxis de los scripts. La incorporación no implica haber instalado sus dependencias ni regenerado el video.
