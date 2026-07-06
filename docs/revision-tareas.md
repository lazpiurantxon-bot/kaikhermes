# Revisión de base de código: problemas detectados y tareas propuestas

Esta revisión identifica cuatro tareas pequeñas y accionables en el área `archive/pre-hermes-services`, cada una orientada a un tipo distinto de mejora: error tipográfico, fallo funcional, discrepancia de comentario/documentación y mejora de prueba.

## 1. Corregir un error tipográfico en la ayuda del gateway

- **Problema detectado:** el texto de ayuda de `gateway.py` usa el verbo `rearmar` para describir `REANUDA`. En el resto del sistema el concepto operativo es “reanudar” la ejecución tras una pausa, por lo que `rearmar` puede resultar ambiguo para un operador no técnico.
- **Archivo afectado:** `archive/pre-hermes-services/gateway-telegram/gateway.py`.
- **Tarea propuesta:** cambiar la descripción de `REANUDA` en `AYUDA` a una formulación explícita como `reanudar tras kill switch`.
- **Criterio de aceptación:** al enviar un comando no reconocido, la ayuda muestra `REANUDA — reanudar tras kill switch` o una frase equivalente, sin cambiar el comportamiento del comando.

## 2. Solucionar un fallo al consultar healthchecks con URL inválida o sin esquema

- **Problema detectado:** `watchdog.py` consume `HEALTH_URLS` directamente desde el entorno y llama a `urllib.request.urlopen(url, timeout=10)`. Si una entrada está vacía tras normalización parcial, no tiene esquema (`example.com/health`) o contiene espacios accidentales, el watchdog genera alertas poco accionables o intenta abrir valores inválidos.
- **Archivo afectado:** `archive/pre-hermes-services/watchdog/watchdog.py`.
- **Tarea propuesta:** normalizar cada URL con `strip()`, validar que incluya esquema HTTP/HTTPS antes de llamar a `urlopen` y emitir una alerta específica para entradas inválidas.
- **Criterio de aceptación:** con `HEALTH_URLS=" example.com/health,https://ok.example/health "`, el watchdog no intenta abrir `example.com/health` y encola una alerta clara indicando configuración inválida.

## 3. Corregir una discrepancia entre comentario/documentación y comportamiento de backups

- **Problema detectado:** la documentación de `watchdog.py` dice que el servicio realiza una “copia local rotada”, pero la rotación elimina cualquier nombre listado en `BACKUP_DIR`, no solo backups de la base de datos. Si el directorio contiene otros archivos auxiliares, podrían borrarse por accidente.
- **Archivo afectado:** `archive/pre-hermes-services/watchdog/watchdog.py`.
- **Tarea propuesta:** alinear documentación y código: o bien documentar que `BACKUP_DIR` debe ser exclusivo para backups `mandi-*.db`, o preferiblemente cambiar la rotación para filtrar solo archivos con prefijo `mandi-` y sufijo `.db`.
- **Criterio de aceptación:** la rotación conserva archivos no relacionados en `BACKUP_DIR` y el comentario/docstring describe exactamente qué archivos se rotan.

## 4. Mejorar la prueba del kill switch para cubrir comandos reales del gateway

- **Problema detectado:** `test_kill_switch.py` valida el contrato de pausa llamando directamente a `gateway.set_pausa`, pero no ejercita `gateway.handle` con los comandos reales `PARA TODO` y `REANUDA`. Por eso podría romperse el enrutamiento de comandos sin que la prueba lo detecte.
- **Archivo afectado:** `archive/pre-hermes-services/tests/test_kill_switch.py`.
- **Tarea propuesta:** parchear o sustituir `gateway.send` durante la prueba para evitar red, invocar `gateway.handle(con, "PARA TODO")` y `gateway.handle(con, "REANUDA")`, y verificar tanto el estado `pausado` como los mensajes producidos.
- **Criterio de aceptación:** la prueba falla si `handle` deja de reconocer `PARA TODO` o `REANUDA`, y sigue ejecutándose en local/CI sin acceso a Telegram.
