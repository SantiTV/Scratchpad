# MEMORY.md — Obsidian Quick Notes Sync
Memoria del proyecto entre sesiones. Máximo ~50 líneas: resume o elimina lo que ya no aporte.

## Estado actual
- Transición de Notion a Obsidian y Google Drive definida.
- Requisito técnico clave establecido: prohibido usar FastAPI.
- Planificación del borrador de la interfaz web minimalista con selección manual (checkboxes) para sincronización dual.

## Decisiones (y por qué)
- Uso de Python estándar / framework ligero (sin FastAPI): mantener la arquitectura simple, rápida y sin sobreingeniería para un entorno local.
- Sincronización dual selectiva (Local y Google Drive): otorga control total al usuario sobre qué apuntes rápidos se guardan en la bóveda de Obsidian o en la nube.

## Aprendizajes y errores a evitar
- (vacío por ahora)

## Próximos pasos
- Escribir la estructura base de `app.py` y el frontend estático para la captura de notas en Markdown.
- Configurar la escritura directa de archivos en la ruta de la bóveda local de Obsidian.
- Integrar la autenticación y subida selectiva hacia la API de Google Drive.