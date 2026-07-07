# Núcleo determinista de la oficina Hermes (tablero + política de marcas).
# La inteligencia vive en Hermes Agent (skills, subagentes, cron); este paquete
# solo implementa lo que la gobernanza exige que sea determinista (doc 06 §4):
# tablero auditable, política de marcas fail-closed, WIP, breakers y ledger.
# Stdlib únicamente: lo usan el CLI `oficina` (herramienta de los agentes)
# y el panel web del propietario.
