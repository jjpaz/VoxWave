# Decisiones

### D038 — 2026-10-11 — Entrada del equipo desde satélite hasta el puente
El propietario elige probar primero el recorrido completo aportado, frente a la simplificación propuesta. Aprueba priorizar pose/ropa/composición de su foto, recorte 16:9 desde muslos conservando caras y skyline, título “The voices behind VoxWave”, nombres y funciones reales alineados con cada integrante y música creciente que resuelve al llegar. Prompts preparados en `video/script/team-intro-v01.md`; recorte exacto local sin generación de rostros. La fotografía personal se mantiene excluida de Git. Permiso de carga al proveedor y derechos pendientes de confirmar; la autorización de referencias sintéticas anterior no se extiende automáticamente a esta foto. Sin cambios a plataforma/hardware ni nueva elección de proveedor.


### D037 — 2026-10-10 — Montaje completo, antialiasing y equilibrio de sonido
El propietario solicita montar la apertura completa, comprobar coherencia/sincronía y reducir protagonismo del ambiente; señala dientes de sierra en la onda. Se comprueba aliasing en un fotograma del MP4 v07, no únicamente en preview. v08 conserva medios y frases: contorno continuo de waveform a 4× reducido a 720p, texto a 3× y logo a 4×; envolvente de audio con ataque 85 ms/liberación 240 ms y eliminación de la inercia adicional de 1,25 s del narrador. Se mantienen contornos/colores/letras del cierre sin declararlo aprobado. La pregunta comienza 0,65 s tras la última intervención; cola final se desplaza 0,4 s (total 72,2 s). Ambientes ajustados hacia −48 dBFS RMS antes de fundidos/ducking, picos limitados y atenuación durante voz; compresión suave de llamada y narrador reducido para evitar salto excesivo. Mezcla 48 kHz estéreo. No nueva generación ni cambio de proveedor. Artefactos locales ignorados; notas en `video/editing/opening-v08.md`.

### D036 — 2026-10-10 — Revisión del teléfono a 720p
El propietario autoriza regenerar M01 y corrige explícitamente la propuesta de 1080p: continuar a 720p de momento. Mano inicialmente fuera del plano, timbre, entrada con temblor más visible y recogida; la conversación empieza después de responder. Seedance 2.5, 8 s con audio, una generación: 1,737 USD. Se edita con imagegen el primer fotograma aprobado para retirar mano y manga. Timbre añadido localmente para controlar su corte (3,9 s), saludo a 5,8 s tras salida del móvil. M01 se prolonga con 0,8 s de mesa vacía hasta 8,8 s en montaje. Se desplazan conversación, tarjetas y cierre 2,8 s de forma conjunta sin recortar pausas. M02–M04 reutilizados con ambientes 10 dB más bajos que v06. Cierre y voces no regenerados; revisión artística pendiente. Véase `video/editing/phone-revision-v02.md`.
| ID | Fecha | Decisión | Motivo |
|---|---|---|---|
| D023 | 2026-10-10 | Recuperar contornos del original, efecto suave y voces a velocidad nativa | Rechazo de v03 y nuevas fuentes del propietario |
| D001 | 2026-10-08 | Foco exclusivo en Parkinson | Instrucción del propietario |
| D002 | 2026-10-08 | Screening por voz; sin afirmar diagnóstico | Alcance del proyecto |
| D003 | 2026-10-08 | Flujo principal diseñado para offline | Requisito prioritario |
| D004 | 2026-10-08 | Un repositorio con video, platform, hardware y docs | Contexto compartido y trabajo separado |
| D005 | 2026-10-08 | GitHub privado; sin datasets ni audio clínico | Instrucción del propietario |
| D006 | 2026-10-08 | Stack y hardware aún abiertos | Evitar decisiones prematuras |
| D007 | 2026-10-08 | Incorporar el material previo de video y logo al mismo repositorio que la plataforma | Solicitud explícita del propietario; se preservan los originales locales y se revisan los archivos antes de subirlos |
| D008 | 2026-10-08 | Permitir solo el MP4 del logo como excepción a la exclusión general de videos | Recurso gráfico revisado de 839300 bytes; los demás renders siguen excluidos |
| D009 | 2026-10-08 | Integrar el contenido de voxwave-video-pitch como parte del repositorio privado VoxWave | El propietario pidió reunir video y desarrollo en GitHub; se conserva la referencia al repositorio público de origen |
| D010 | 2026-10-08 | Versionar la locución y efectos del pitch integrados | Son recursos audiovisuales ya presentes en el clon, sin audio clínico; las exclusiones generales de audio no aplican a estas rutas revisadas |
| D011 | 2026-10-08 | Usar el SVG oficial recibido como fuente canónica del logo | Evita que README, pitch, dispositivo y assets estáticos diverjan; la fuente vectorizada anterior queda aislada para conservar el renderizador histórico |
| D012 | 2026-10-09 | Estructurar el vídeo con apertura cinematográfica, transición de waveform a logo sobre blanco, explicación animada de producto/problema, marketing y finanzas, y presentación final del equipo | Dirección explícita del propietario; el cambio a azules, naranja y blanco y a mayor movimiento comunica la llegada de la solución. No se eligieron variantes de textos, planos intermedios ni cierre: siguen abiertas. El bloque Remotion existente es material adaptable y no determina la duración ni el montaje completos |
| D013 | 2026-10-09 | Limitar la contribución del propietario a la apertura de 40–50 s, con 2–4 planos sin rostro, todo texto y audio en inglés y mensajes como foco principal | Corrección explícita del propietario: llamada cotidiana con su hija como fondo y fuente de movimiento de la waveform. Sustituye las propuestas de rostro, diálogo protagonista e idioma pendiente de v0.1. Planos adicionales de soledad/distancia/ruralidad y mensajes concretos aún abiertos |

Registrar cada nueva decisión con alternativas, motivo y consecuencias. La arquitectura actual es una propuesta, no implementación.

### D022 — 2026-10-10 — Narrador y transformación propia de marca
El propietario pide combinar música+ambientes y rehacer la transición al logo. Autoriza narrador masculino de ejemplo hasta disponer de Edward, frase que responda a la pregunta y anime la onda, seguida de “Meet VoxWave” durante la transformación. Solicita fluctuaciones previas más largas, letras subiendo en onda y pruebas de efecto orgánico/tecnológico. Se mantiene provisionalmente la despedida antes de la pregunta. Se prueba George y “In the voices we hear every day.” como copy propuesto; no se fija narrador ni frase final. La animación usa geometría del SVG oficial y no altera el archivo canónico. Maqueta v03 de 69 s, duración de trabajo flexible.

### D021 — 2026-10-10 — Ritmo flexible y cierre anterior al logo
El propietario aclara que 50 s es orientativo y pide que la llamada termine antes del logo, sustituyendo el cierre anterior sobre la transición. Confirma “What if the answer was always there?”, textos actuales, llamada más de fondo, waveform más gruesa y suave, y planos más largos. Autoriza probar despedida antes/durante la pregunta, ambientes/música sutil y ajustes de transición. La revisión de entonación y pausas queda para después. Maqueta v02 de 63 s con cuatro combinaciones; 63 s es una propuesta de montaje, no nueva duración obligatoria. Detalles en `video/editing/opening-animatic-v02.md`.

### D020 — 2026-10-10 — Primera maqueta visual local
El propietario autoriza montar la maqueta de 50 s con textos, waveform y planos provisionales antes de generar los planos Seedance. Se usa la conversación v02 y la parte final de su referencia de logo. Para entregar la primera revisión sin instalar las dependencias ausentes de Remotion, se renderiza con Pillow/FFmpeg ya disponibles; es una decisión de producción de la maqueta, no un cambio del stack del producto ni de la elección de Seedance. El proyecto Remotion integrado se conserva. Dibujos esquemáticos sustituyen temporalmente los cuatro planos; no se presentan como metraje final. Detalles y límites en `video/editing/opening-animatic-v01.md`.

### D019 — 2026-10-10 — Voz materna y tratamiento de la llamada
Última selección del propietario: hija `ogwqBH5bbF03DSbNiRNN` en lugar de Sarah; madre `5u41aNhyCU6hXOcjPPv0`. Conversación completa regenerada como v02; v01 se conserva como referencia. Continúan ritmo pausado, matices y filtro común a ambas voces.

Actualización: el propietario aprueba la prueba v02 con la nueva voz y Sarah y autoriza continuar. Se genera una toma completa y se conserva sin editar; el montaje local añade pausas y usa velocidad 0,92 sin cambiar tono para entregar una escena de 50 s. Filtro en ambas voces; timbre provisional, pendiente de sincronización al plano.

Tras escuchar la primera prueba, el propietario elige la voz ElevenLabs `5u41aNhyCU6hXOcjPPv0` para sustituir a Julie. Pide conversación final más pausada y con más matices y filtro telefónico en ambas personas. Sarah continúa como candidata de hija; conservar máster limpio y aplicar el filtro sobre la mezcla completa. Mantener el objetivo de escena de 50 s, pendiente de medición del diálogo completo.

### D018 — 2026-10-10 — Servicios para preparar la apertura
El propietario elige Seedance para los planos, dispone de ElevenLabs y configura las claves de ElevenLabs y APIMart para iniciar la comprobación. Se prepara el acceso a Seedance mediante APIMart, frente a las alternativas de interfaz web o API directa de BytePlus; no se fija todavía la versión de Seedance. La consulta de voces de ElevenLabs funciona; APIMart responde con saldo insuficiente. Esta elección se limita a producción audiovisual y no cambia la arquitectura offline del producto. Casting propuesto y estado de conexión en `video/script/voice-casting.md`; aún no hay generación de medios.

### D016 — 2026-10-09 — Referencia audiovisual de waveform a logo
El propietario aporta `voxwave_logo_reveal DEFINITIVO.mp4` como referencia para la transformación de la waveform en el logo y solicita conservarlo. Se guarda una copia local en `video/references/motion/`, conservando el original en Descargas, en lugar de sustituir los assets existentes. El vídeo sigue excluido de Git y no se amplía la excepción de medios; el SVG oficial continúa siendo la fuente canónica del logo.

### D014 — 2026-10-09 — Enfoque informativo y geográfico
El propietario elige magnitud, detección tardía y acceso como las tres pantallas de datos, con una pregunta final sobre la voz. Ambos problemas, detección y acceso, son importantes. Define TAM mundial, SAM países bálticos y SOM Lituania como ámbitos geográficos; cifras de mercado y datos médicos no están calculados ni aprobados. Esta elección sustituye la alternativa de mensajes puramente emocionales. El guion reserva una cuarta tarjeta breve de transición; redacción exacta y fuentes siguen pendientes.

## Propuestas pendientes de revisión — 2026-10-09
Corrección del propietario sobre audio: eliminar desayuno, preguntar cómo está/se encuentra y dar un motivo coherente a la despedida, por ejemplo volver al trabajo. Solicita 50 s. Se reemplaza el diálogo anterior en `video/script/voiceover.md`; se propone solapar despedida y logo para conservar la apertura de 50 s. Tiempos de interpretación pendientes de medición.

Actualización de conversación: el propietario acepta la propuesta anterior y solicita una llamada coherente que empiece y termine, con posible referencia a pedir cita médica. Se propone conversación madre/hija de unos 40 s, documentada en `video/script/voiceover.md`; texto exacto, voces y mezcla pendientes de prueba. No se convierte el diálogo ficticio en evidencia clínica.

### D017 — 2026-10-09 — Cuatro frases completas en la apertura
El propietario solicita explícitamente conservar las cuatro frases de la selección, incluida la frase completa sobre fastest-growing y proyección superior a 25 millones para 2050. Sustituye las propuestas de recortar esa frase o seleccionar solo una afirmación de magnitud. El mapa de trabajo v0.3 reserva cuatro tarjetas informativas y mantiene la pregunta final; los 50 s y encuadres siguen siendo propuesta de montaje. Mantener las fuentes y su alcance documentados en `video/script/opening-copy-shortlist.md`.

El propietario prefiere combinar sala de espera, pasillo médico, carretera rural y detalles de casa (ventana, taza, sillón con manta, pasillo). Se propone agruparlos en cuatro planos y 50 s dentro de D013; no se da por aprobado cada encuadre. Prompts añadidos al documento v0.3, manteniendo las variantes anteriores como referencia.

Preferencias de texto: el propietario destaca las frases de esperas de meses, reconocimiento tardío de síntomas, estimación mundial superior a 10 millones y crecimiento con proyección superior a 25 millones en 2050. Fuentes y matices documentados en `video/script/opening-copy-shortlist.md`. La selección definitiva, el superlativo y una posible duración de 49 s no quedan aprobados por esta preferencia.

### D015 — 2026-10-09 — Producción de apertura con IA
El propietario confirma entorno rural báltico, móvil antiguo de botones tipo Nokia (no smartphone) y generación íntegra mediante IA; solicita guion técnico en formato prompt. Esto sustituye las alternativas de rodaje o producción mixta. No selecciona proveedor ni cambia el stack de plataforma. Los prompts proponen tres planos y composición separada para textos, waveform y logo exactos; detalles de casa, estación y vestuario siguen siendo propuestas creativas.

La apertura activa es `video/script/cinematic-opening-v02.md`: propone 45 s y tres planos (teléfono, mesa con silla vacía y exterior rural). D013 prevalece sobre las propuestas históricas siguientes; ni estos planos concretos ni los textos nuevos están aprobados.

El guion técnico v0.1 desarrolla D012 con una duración provisional de tres minutos, tres tarjetas en la apertura y presentación del equipo trabajando. Propone separar la llamada narrativa de la captura guiada consentida, incorporar control de calidad y reservar el seguimiento longitudinal del bloque previo hasta aclarar su alcance. No se han aprobado estas elecciones como montaje final ni seleccionado nuevos proveedores, stack o hardware. Ver `video/script/technical-script-v01.md` para alternativas y campos pendientes.

### D023 — 2026-10-10 — Revisión de animación y voces
El propietario rechaza v03 y el carácter robótico de las voces. Se revisan sin ejecutar las fuentes entregadas y se copian en `video/references/motion/original-source/`. La adaptación recupera contornos cerrados, entrada escalonada de azul/navy, sincronización y transformación al perímetro antes del relleno; conserva SVG oficial y prolonga la fase previa 1,2 s. Se mantiene entrada ondulada de letras. Efecto suave elegido; variante tecnológica descartada para esta prueba.

Se regeneran conversación y narración sin etiquetas de lentitud. Madre e hija conservan IDs elegidos; George continúa provisional. Sin atempo ni silencios insertados entre respuestas. Despedida antes de pregunta; la toma más corta deja un tramo mayor de música y ambiente. Ritmo y encaje pendientes de escucha; no se fuerzan 50 s.

### D024 — Restaurar conversación pausada; correcciones puntuales
2026-10-10: el propietario pide recuperar la conversación pausada anterior. Base activa: conversación v02 de 50 s, con los IDs elegidos de madre e hija, pausas y filtro telefónico. Se descarta como base la toma corta v03. Corregir solo entonaciones concretas tras identificarlas. La sincronía y transformación del logo v04 siguen pendientes; no se consideran aprobadas. La versión v05 restaura también la waveform calculada para esta conversación. Se conserva música, ambiente, efecto suave y cierre v04 sin darlo por aprobado. Sin regeneración de voces ni cambios a los planos.

### D025 — 2026-10-10 — Imagen de referencia antes de animar M01
El propietario autoriza el siguiente paso propuesto: fijar primero la estética mediante una imagen del teléfono y mano, antes de gastar generaciones de vídeo. Se usa la herramienta integrada de imágenes para esta referencia; Seedance sigue siendo el proveedor elegido para movimiento, sin cambio definitivo de proveedor de vídeo ni del stack de producto. Archivo local ignorado, sin subir imágenes privadas o clínicas. La estética de v01 queda pendiente de selección del propietario.

### D026 — 2026-10-10 — Luz nublada y ambiente melancólico
2026-10-10: el propietario pide M01 más oscuro, con menos luz general y luz de ventana de día nublado, para transmitir soledad y melancolía. Referencia v02 editada con la herramienta integrada, conservando encuadre y objetos; guardada en `video/renders/keyframes/m01-phone-reference-v02.png`. Revisada visualmente: fondo más oscuro, menor calidez y mano/teléfono legibles; selección final pendiente. Mantener esta dirección lumínica en los planos siguientes. Sin generación de movimiento todavía.

### D027 — 2026-10-10 — Móvil actual y comparación de encuadres
2026-10-10: referencias M01 v03 A (oblicua) y B (cenital) generadas con herramienta integrada. Móvil sencillo actual estilo Nokia, pantalla pequeña en color y teclado físico; sin taza, misma oscuridad aprobada. Archivos en `video/renders/keyframes/m01-v03-{A-oblique,B-overhead}.png`. Revisadas visualmente; elección de encuadre pendiente. No se genera vídeo por instrucción del propietario. El propietario confirma temblor visible pero contenido, casa rural cuidada y luz oscura nublada; segundo plano centrado en ventana/paisaje con sillón secundario. Admite acercamiento muy lento. Sustituye el móvil retro de versiones anteriores.

### D028 — 2026-10-10 — Encuadre oblicuo aprobado
2026-10-10: el propietario elige explícitamente M01 v03 A, encuadre oblicuo, mediante la imagen exec-b23c99e8-2677-4f24-a1d6-4c4b34cd6a7f.png. Coincidencia con `video/renders/keyframes/m01-v03-A-oblique.png` verificada por SHA-256. Referencia del primer plano aprobada: móvil actual de botones, sin taza, luz oscura nublada. La opción cenital se conserva como alternativa descartada; no se autoriza todavía generar vídeo.

### D029 — 2026-10-10 — Referencia del segundo plano
2026-10-10: M02 v01 generada como imagen de referencia con la herramienta integrada, usando M01 A para continuidad visual. Ventana y paisaje rural nublado como protagonistas; sillón vacío y manta en sombra a la derecha, mesa en primer término. Guardada en `video/renders/keyframes/m02-window-reference-v01.png`. Revisada visualmente: sin personas ni teléfono, paisaje legible, interior oscuro. Pendiente de revisión del propietario; sin vídeo Seedance. Se sigue la elección del propietario de priorizar ventana y exterior sobre el sillón. Esta generación no fija por sí sola el encuadre final.

### D030 — 2026-10-10 — Taza en el segundo plano
2026-10-10: a petición del propietario, añadida una taza discreta en la mesa del segundo plano. M02 v02 guardada en `video/renders/keyframes/m02-window-reference-v02-cup.png`, edición mediante herramienta integrada. Revisada visualmente: taza en primer término, ventana/paisaje siguen dominando; interior oscuro, sillón y manta conservados. M01 continúa sin taza. Sin generación de vídeo. La prohibición de taza se limita al encuadre cerrado de M01.

### D031 — 2026-10-10 — M02 aprobado y referencia exterior M03
2026-10-10: propietario aprueba M02 v02 con taza. Generada referencia M03 v01 de carretera secundaria asfaltada vacía, campos y abedules con cielo cubierto, usando M02 para continuidad de paisaje/paleta. Imagen en `video/renders/keyframes/m03-road-reference-v01.png`; revisada visualmente sin personas, tráfico o texto. Exterior naturalmente más luminoso que interior; conserva día nublado y tonos apagados. M03 pendiente de selección del propietario. Sin vídeo generado.

### D032 — 2026-10-10 — Alternativas rurales para M03
2026-10-10: el propietario rechaza la carretera M03 v01 y solicita tres alternativas de pueblo rural báltico. Generadas con herramienta integrada y referencia M02: A calle del pueblo, B vista desde la entrada de casa, C plano general entre campos. Archivos `video/renders/keyframes/m03-v02-{A-village-street,B-house-entry,C-village-fields}.png`. Revisadas visualmente: tres composiciones diferenciadas, cielo nublado, paleta apagada, sin personas. Selección pendiente; solo imágenes, sin vídeo. Las tres imágenes son opciones del mismo plano, no tres nuevos planos añadidos al montaje.

### D033 — 2026-10-10 — Pueblo aprobado y referencia de espera
2026-10-10: el propietario elige M03 v02 C, plano general del pueblo entre campos, y autoriza continuar con referencias. Generada M04 v01: cuatro sillas vacías junto a un pasillo y puerta de consulta cerrada, centro modesto y cuidado, luz fría de ventana. Guardada en `video/renders/keyframes/m04-clinic-reference-v01.png`. Revisada visualmente sin personas ni texto; M04 pendiente de aprobación. No se ha generado vídeo. M03 C sustituye la carretera y las alternativas A/B. El centro es ficticio; la imagen ilustra espera sin documentar la actividad ni tiempos de un centro real.

### D034 — 2026-10-10 — Centro médico más frío y apagado
2026-10-10: M04 v02 editada a petición del propietario para luz más fría, menor luminosidad y ambiente más apagado/melancólico. Conserva composición, cuatro sillas, puertas y centro cuidado. Archivo `video/renders/keyframes/m04-clinic-reference-v02-cool.png`; revisión visual confirma menor calidez y sombras más profundas con detalle. Pendiente de selección del propietario. Sin vídeo.

### D035 — 2026-10-10 — Seedance 2.5 y sonido ambiente
2026-10-10: el propietario autoriza pasar a vídeo y elige explícitamente Seedance 2.5 con audio ambiente (viento en exterior). Preparadas cuatro solicitudes 720p, primera imagen como first_frame, formato adaptive, 6/5/5/5 s, audio activado; sin voces ni música generadas. M04 v02 se toma como base al autorizar el siguiente paso. API configurada, saldo inicial 10 USD, estimación orientativa por tarifa publicada 4,536 USD para 21 s; cargo efectivo pendiente de cada tarea. Las referencias son sintéticas revisadas; se autoriza su carga a APIMart para este trabajo. Sin datos clínicos ni voz real. Guardar vídeo original y extraer pista de ambiente para mezcla posterior. No regenerar llamada ni transición del logo en este paso.

Actualización D035: 2026-10-10: completadas y guardadas las cuatro generaciones Seedance 2.5 con audio. Duraciones 6,048/5,056/5,056/5,056 s; coste efectivo total 4,572 USD. Decodificación y pista de audio verificadas; hojas de contacto revisadas. Ambientes extraídos por separado. Reel de 21 s y montaje v06 de 69 s con los cuatro planos en lugar de bocetos; mantiene llamada pausada y cierre aún pendiente de corrección. Revisión artística/escucha del propietario pendiente. Detalles: `video/editing/seedance25-first-shots.md`.

### D036 — 2026-10-11 — Entrega editable v08
Por solicitud del propietario se prepara la entrega de scripts y medios, sin Shotcut. Excepciones explícitas en .gitignore y .gitattributes para 24 medios sintéticos revisados y cinco metadatos; los binarios se almacenan con LFS, incluidos los mayores de 5 MiB. No se amplía la exclusión de material clínico/privado ni se reescribe historial. El repositorio público de Marco recibirá solo una contribución audiovisual aislada, nunca el historial privado completo.
