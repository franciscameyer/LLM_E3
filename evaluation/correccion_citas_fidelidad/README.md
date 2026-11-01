# Evidencia de corrección de P07 y A04

Fecha: 2026-11-01. Evidencia técnica, no informe académico ni presentación.

- `pruebas.xml`: 40 pruebas aprobadas, incluyendo casos nuevos de contexto,
  referencias desconocidas, resolución exacta y abstención de credenciales.
- `repeticiones/resultados.json`: intento intermedio con recuperación desde el
  motivo del caso, todavía sin referencias cortas. P07 falló 3/3; A04 pasó 3/3.
- `referencias_cortas/resultados.json`: primera verificación de referencias exactas
  F1/F2 resueltas a fuentes originales; ambos casos pasaron las tres repeticiones.
- `verificacion_final/resultados.json`: código final, tres repeticiones de cada
  caso con sesiones distintas y base temporal. P07 responde con POL-DEC v2 §6,
  sin reintento de citas. A04 es abstención controlada, sin invocar al modelo ni
  inventar recuperación de acceso.
- `revision_dirigida_agente.json`: revisión factual de las seis salidas. Registra
  sobrecitación en P07: los hechos de la ficha sí vienen de MCP, pero una cita
  documental adicional no respalda esos datos vivos. No se declara precisión perfecta.
- `verificacion_general.json`: cliente MCP externo y ocho consultas de casos,
  permisos y reglas con la versión corregida. Conservar sus resultados por consulta;
  no convertir ausencia de errores estructurales en fidelidad semántica automática.
- `resumen.json`: resultados y huellas del cierre de esta corrección.

La evaluación completa posterior se guarda en `evaluation/ejecucion_05/` con su
propia revisión semántica automatizada y muestra humana aún sin completar.
El golden y el kit originales no se modifican; las aprobaciones del cliente y
del docente permanecen pendientes según `docs/validaciones-pendientes.md`.

Reproducción desde la raíz con Bonsai encendido:

```powershell
.\.venv\Scripts\python.exe -m mira.regression_check --salida .cache/regresion-nueva --repeticiones 3
.\.venv\Scripts\python.exe -m mira.cli evaluar --generacion --salida evaluation/ejecucion_nueva
.\.venv\Scripts\python.exe -m pytest -q
```
