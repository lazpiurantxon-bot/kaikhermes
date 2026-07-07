---
name: outreach-r3
description: Proceso completo de contacto con terceros reales (proveedores, atletas, salas, clientes) - borrador personalizado, gate R3 individual, y envío SIEMPRE por el propietario. El sistema no envía nada a nadie.
---

# Outreach a terceros (R3)

Nivel de modelo: 2. **Regla de hierro del acta B4(c): el sistema no contacta con terceros. Prepara; el propietario envía.**

## Procedimiento

1. Verifica el destinatario: web viva, email/formulario de contacto correcto, persona/rol adecuado. Datos con fuente y fecha en la ficha (`knowledge/<dominio>/`).
2. Personaliza el borrador desde la plantilla del dominio (p. ej. `domains/ezti/outreach/borrador-contacto-copacker-ES.md`): nombre, referencias específicas de esa empresa, idioma correcto (ES para España; EN para UE/internacional).
3. Si el texto es público-facing de EZTI, pasa antes `ezti-claims`.
4. Solicita gate R3 **individual por destinatario** vía `jdg-gate` — nunca "apruebas el lote". El gate incluye: destinatario, borrador completo, y qué se espera de la respuesta.
5. Con `APRUEBO`: entrega al propietario el paquete listo (destinatario + asunto + cuerpo) por Telegram, formateado para copiar-pegar-enviar en 30 segundos. **Y ahí termina tu trabajo: el envío es suyo.**
6. Dominio música: BLOQUEADO por completo hasta resolver E13 — ni siquiera con gate (playbook del dominio). Dominio hotel: el sistema jamás contacta al empleador — sin excepción posible.
7. Registra en la ficha del destinatario: enviado (fecha, por el propietario), respuesta, siguiente paso. Las respuestas alimentan el scoring (EZTI) o el pipeline correspondiente.
