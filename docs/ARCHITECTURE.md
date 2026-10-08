# Arquitectura propuesta
Estado: diseño inicial, sin implementación ni stack decidido.

## Flujo principal offline
Frontend/mobile → consentimiento y grabación local → preprocessing → features → inference con modelo local → resultado orientativo o no concluyente.

- preprocessing: calidad, segmentación y normalización con parámetros versionados.
- features: extracción reproducible y contrato de características.
- models: código y fichas de modelos; pesos fuera de Git, con procedencia y licencia.
- inference: carga local, versionado y tratamiento de errores.
- frontend y mobile: interfaces; definir cuál será el primer cliente antes de implementar.
- api: contratos compartidos y límites entre componentes.
- backend: servicios opcionales; ninguna carga de audio automática.
- tests: muestras sintéticas, fallos de micrófono, baja calidad, ausencia de red y compatibilidad del modelo.

## Datos
Minimizar persistencia de audio. Definir explícitamente retención, borrado y almacenamiento local antes de trabajar con datos reales. Sin sincronización implícita ni telemetría clínica.

## Hardware
Exploración independiente: ESP32, micrófono, carcasa y BOM no implican selección final. La inferencia en ESP32 no se da por viable sin medir recursos.

## Video
Guion → storyboard → prompts → assets autorizados → edición → renders locales. No transmitir datos clínicos a Seedance ni a generación de imagen.
