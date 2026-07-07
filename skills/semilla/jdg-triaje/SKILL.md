---
name: jdg-triaje
description: Clasificar todo intake entrante (Telegram, issues, retro) en dominio, nivel de riesgo R0-R3 y prioridad; crear o actualizar el issue correspondiente. Usar siempre que llegue una idea, petición o señal nueva.
---

# Triaje (Jefe de Gabinete)

Nivel de modelo: 1-2 (rutina).

## Procedimiento

1. Lee el intake. Identifica: dominio (`ezti|core|musica|hotel|nuevo`), tipo (idea/tarea/bug/pregunta/señal), y si duplica un issue existente (busca antes de crear).
2. Clasifica riesgo según `operating-model/06` §1. **Ante duda entre dos niveles, el superior.** Recuerda los prohibidos: si el intake pide algo de la lista de prohibidos (Tier-0, fiscal con presentación, firma, datos del hotel, publicar música), NO se triaja: se responde que no existe ruta para eso y se registra.
3. Si el dominio es `musica` u `hotel`, aplica su playbook antes de nada (bloqueos E13/E12).
4. Crea/actualiza el issue con el bloque de estado de `playbooks/tablero.md` y prioridad razonada en una línea.
5. Prioridad por defecto: EZTI > core > resto (acta H23). El propietario puede reordenar con un mensaje.
6. Respeta el WIP limit: máximo 2 iniciativas en BUILD/QA/DEPLOY. Lo nuevo espera en cola, no arranca.
7. Confirma al propietario en una línea: qué se registró, dónde, y cuándo se moverá.
