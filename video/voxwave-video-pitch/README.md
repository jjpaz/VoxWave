# VoxWave video pitch

Snapshot integrado desde [MarcoGarLop/voxwave-video-pitch](https://github.com/MarcoGarLop/voxwave-video-pitch) el 2026-10-08.

Es un proyecto Remotion con React y TypeScript para el bloque de solución del pitch de Creative Shock. Contiene ocho escenas (`s01`–`s08`), locución y efectos, interfaces animadas, y scripts de Blender para el dispositivo. La duración configurada es de 55 segundos a 30 fps.

Los datos, métricas, pacientes y señales son simulados para el vídeo. Este proyecto no implementa el análisis clínico de Parkinson.

El logo oficial está disponible en `public/logo-oficial.svg` y `public/logo-original.svg`. Las escenas SVG usan la misma geometría y la paleta oficial definida en `src/brand/tokens.ts`.

## Uso

Desde esta carpeta:

```sh
npm install
npm run typecheck
npm run dev
```

Para un render del bloque completo:

```sh
npm run render -- Block2 out/block2.mp4
```

El render 3D necesita Blender 5.x. Las dependencias de Node y las herramientas externas no se instalan automáticamente en el entorno principal de VoxWave.

El snapshot está dentro del repositorio privado principal. Los cambios posteriores deben hacerse aquí y publicarse desde `VoxWave`; el repositorio público de origen se conserva como referencia, no como remoto de publicación de este proyecto.
