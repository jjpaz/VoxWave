# Apertura completa — v08

2026-10-10. Solicitud: montar la apertura entera, comprobar coherencia y sincronía, suavizar waveform y mantener ambientes discretos. Sin API ni regeneraciones. Se conservan las voces actuales con sus pausas y el texto completo de las cuatro tarjetas.

## Entrega

`video/renders/VoxWave-opening-v08-720p.mp4` — 72,2 s, 1280×720, 30 fps, H.264 CRF 15, AAC estéreo 48 kHz/192 kbps. Mezcla previa sin pérdida: `video/renders/v08/mix.wav`, PCM 24 bits. Fuentes y versiones anteriores conservadas. Todos estos archivos quedan ignorados por Git.

## Orden y sincronía

| Tiempo | Imagen / sonido |
|---|---|
| 0–8,8 s | Móvil solo, timbre, mano entra y recoge. Timbre corta a 3,9 s; saludo a 5,8 s después de salir el móvil. |
| 8,8–13,8 s | Tarjeta de magnitud. |
| 13,8–18,8 s | Ventana, sillón y taza. |
| 18,8–29,8 s | Crecimiento y proyección de 2050. |
| 29,8–34,8 s | Pueblo báltico entre campos. |
| 34,8–39,8 s | Reconocimiento de síntomas. |
| 39,8–44,8 s | Espera en centro médico. |
| 44,8–53,2 s | Acceso al especialista. La conversación termina a 52,55 s. |
| 53,2–59,2 s | “What if the answer was always there?” |
| 59,2–72,2 s | Onda y cierre. Narración a 60,8 s; “Meet VoxWave” a 66 s, durante transformación. |

La llamada conserva once intervenciones. El saludo, pregunta por el estado de la madre, cita pendiente, ofrecimiento de acompañar y despedida para volver al trabajo forman una conversación completa. El logo mantiene los contornos, colores y letras de la adaptación existente; su aprobación artística sigue pendiente. La contribución cubre solo esta apertura, no añade producto/finanzas/equipo.

## Waveform

El MP4 v07 tenía escalones en los bordes: no era solo el reproductor. Se sustituye el trazo hecho con segmentos a resolución final por un contorno continuo rellenado a 4× y reducido con Lanczos. También se renderizan las tarjetas a 3× y el cierre a 4×. El archivo continúa siendo 720p; no se presenta como vídeo generado en 1080p.

Amplitud derivada de RMS del audio real cada 10 ms, interpolación temporal y ataque/liberación de 85/240 ms. No representa la forma física exacta de la señal: es una curva gráfica gobernada por su energía. Después de la despedida se añade silencio al análisis para que la onda se estabilice. Se elimina la inercia adicional de 1,25 s del cierre, que prolongaba el movimiento durante pausas del narrador. Anchura de 6 px continua entre tarjeta y cierre.

## Sonido

Se reconstruye la mezcla desde las pistas separadas. Misma interpretación, filtro telefónico y pausas; compresión ligera para controlar picos sin cortar palabras. Narrador reducido frente a v07, manteniendo mayor presencia que la llamada de fondo. Ambiente de cada plano ajustado hacia −48 dBFS RMS, con picos limitados a aproximadamente −30 dBFS antes de mezcla, fundidos y reducción automática durante voz. Música sostenida muy discreta y efecto orgánico suave.

El timbre está colocado localmente sobre el gesto, no generado junto a las voces. Se mantiene el corte a 3,9 s sobre el pulgar parcialmente oculto; el saludo no entra hasta la salida del móvil. Fondo y narrador no impulsan la onda de las tarjetas; el narrador impulsa la del cierre.

## Comprobaciones reproducibles

Resultado: decodificación completa correcta; 2166 fotogramas y 72,200 s exactos; salida estéreo 48 kHz. Orden de cues, once intervenciones y reposo de la waveform en silencio verificados. Medidas sobre MP4 final: −28,45 LUFS integrados, −9,23 dBTP y 10,50 LU de rango; no clipping. Nivel global deliberadamente discreto para esta apertura. Revisados fotogramas exportados de todos los planos/tarjetas y etapas del cierre, incluidos bordes de onda en el MP4 final.

```powershell
python video/tools/finalize_opening_v08.py
python video/tools/verify_opening_v08.py
python scripts/check_repository.py
```

`video/renders/v08/edit-report.json` registra mezcla y tiempos. `verification.json` registra duración/pistas, decodificación, orden de cues, conservación de las once intervenciones, respuesta de la onda en silencio y loudness/true peak del MP4. `qa-contact.jpg` permite revisar planos, tarjetas y cierre; se revisan además fotogramas del archivo comprimido. La revisión del agente es visual y técnica, no una escucha humana de interpretación.
