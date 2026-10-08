# Codex local y Cloud
## Local
Abrir esta carpeta VoxWave como raíz del proyecto. AGENTS.md contiene las instrucciones compartidas.
Verificar con `python scripts/check_repository.py`. Git usa la rama main.
El scaffold no necesita instalar paquetes, claves API ni herramientas clínicas.

## GitHub
Repositorio privado: https://github.com/jjpaz/VoxWave.
Cuenta: jjpaz. El remoto origin apunta a ese repositorio.
Antes de publicar cambios: revisar `git diff`, ejecutar el comprobador y confirmar que no se incluyan datos privados.
Publicar commits revisados con `git push origin main`. No sobrescribir historia remota.

## Cloud
Entorno VoxWave publicado el 2026-10-08 y conectado a jjpaz/VoxWave. Visibilidad: Only me.
En tareas Cloud, seleccionar VoxWave y la rama main.
Preparación validada con Python 3.12.14, Git y lectura de GitHub. Los 47 archivos superaron el comprobador.
Para este scaffold no se necesitan secretos ni descargas. Comando de comprobación: `python scripts/check_repository.py`.
Acceso a Internet del agente desactivado. No hay scripts de instalación, secretos ni variables de entorno añadidos.
Nunca cargar datos clínicos en tareas Cloud. Revisar necesidades de red al incorporar dependencias.
Cuando se elija stack, añadir versiones fijadas, dependencias y comandos reales de instalación y pruebas.

## Material audiovisual
El mismo repositorio contiene ahora el logo y su animación en video/assets/logo y los scripts en video/tools.
Las tareas Cloud nuevas que utilicen main actualizado podrán acceder a esos archivos. Las copias o tareas ya abiertas necesitan actualizar su rama.
Los scripts audiovisuales requieren NumPy, Pillow y, para render, FFmpeg. No se han instalado esas dependencias en el entorno Cloud; la validación básica del repositorio sigue sin dependencias externas.

Referencias oficiales consultadas el 2026-10-08:
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/environments/cloud-environment
