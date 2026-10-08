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
Tras publicar, conectar GitHub en Codex y habilitar acceso al repositorio privado VoxWave.
Crear o seleccionar un entorno para ese repositorio y rama main.
Para este scaffold no se necesitan secretos ni descargas. Comando de comprobación: `python scripts/check_repository.py`.
Mantener acceso de red limitado a lo necesario. Nunca cargar datos clínicos en tareas Cloud.
La preparación del repositorio no crea por sí sola el entorno ni concede acceso a la cuenta.
Cuando se elija stack, añadir versiones fijadas, dependencias y comandos reales de instalación y pruebas.

Referencias oficiales consultadas el 2026-10-08:
- https://learn.chatgpt.com/docs/agent-configuration/agents-md
- https://learn.chatgpt.com/docs/environments/cloud-environment
