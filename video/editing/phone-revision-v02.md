# Revisión del teléfono — v02

2026-10-10. Seedance 2.5 a 720p, según última indicación explícita. Una generación de 8 segundos (archivo 8,064 s), coste efectivo 1,737 USD. Primer fotograma sin mano creado con imagegen integrado; prompt exacto en `../script/m01-phone-v04-empty-firstframe.md`. Prompt y configuración de vídeo en `../script/seedance25-phone-v02.json`.

## Entregables locales (ignorados por Git)

- `video/renders/m01-phone-v02-synced-720p.mp4`: extracto de 8,8 s con timbre, ambiente suave y entrada de conversación; es un extracto, el diálogo continúa en el montaje completo.
- `video/renders/opening-v07-phone-corrected.mp4`: montaje completo de 71,8 s.
- `video/renders/seedance25-phone-v02/m01/m01-seedance25-v02.mp4`: generación original de 8,064 s, 1280×720 a 24 fps, audio estéreo.
- `video/renders/opening-v07-timing.json`: tiempos y ajustes de mezcla.

## Montaje

El móvil aparece solo inicialmente; la mano entra aproximadamente a 1,5 s. La recogida ocupa aproximadamente 3,5–5,7 s. Corte del timbre a 3,9 s sobre el gesto del pulgar (la tecla está parcialmente oculta; no se presenta como detección automática). Saludo a 5,8 s, tras salir mano y móvil del encuadre. La pantalla del teléfono mantiene su icono, por lo que el sonido explica la respuesta.

La mesa vacía se mantiene hasta 8,8 s (último fotograma prolongado unos 0,8 s). Desplazamiento de 2,8 s del resto del montaje: las once intervenciones, pausas, textos y waveform conservan su relación temporal. Despedida final a 52,55 s, pregunta a 52,8 s y cierre a 58,8 s. Diseño del logo sin modificaciones, todavía pendiente de aprobación.

Nuevo timbre discreto sintetizado localmente; se elimina el anterior. Ambiente M01 a −6 dB respecto a su fuente; M02–M04 diez dB por debajo de la mezcla v06. Base musical y conversación conservadas. No nuevas llamadas a ElevenLabs.

## Reproducción y revisión

`python video/tools/assemble_phone_v02.py --answer 3.9 --call-start 5.8`

Fuente decodificada correctamente, audio presente y secuencia revisada mediante hojas de contacto. Revisar en reproducción la intensidad del temblor y la naturalidad del gesto y sonido: las instrucciones al generador no garantizan cada matiz interpretativo. No se ha realizado una nueva generación adicional.
