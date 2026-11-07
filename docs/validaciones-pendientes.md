# Validaciones y estado del cierre de E3

Actualizado: 7 de noviembre de 2026. Equipo: Francisca Meyer, Lukas Scheel y Sebastian Rodriguez. Representante del cliente: Francisca Meyer.

## Completado

- **VC-01, aprobación del golden:** Francisca Meyer revisó y aprobó las veinte preguntas y expectativas, según confirmación explícita comunicada por el usuario el 07-11-2026. El registro incluye versión y huellas en `evaluation/cierre_v3_20261107/aprobacion_cliente.json`; no se modifica retroactivamente el golden original.
- **VE-02, contraste de antecedentes:** se leyó el capítulo 7 de la Descripción completa de MIRA, el informe de E2 y sus actas de usabilidad. El hash del original coincide con el identificado por los extractos. Hallazgos y límites en `docs/contraste-antecedentes.md`.
- **Verificación actual:** 47 pruebas aprobadas, comparación de fragmentación y cliente MCP externo reejecutados en un entorno temporal separado. No se reinstalaron ajustes de hardware en el proyecto.
- **Muestra técnica:** nueva lectura de ocho respuestas guardadas de ejecución 06: 14/14 citas respaldadas y 8/8 respuestas fieles. Concordancia con la revisión técnica previa: 8/8 en fidelidad, 8/8 en cantidad de citas y 3/3 en conflicto/vigencia. No se detectaron discrepancias en esta muestra.
- **Ensayo sin generación:** nueve escenarios de API y revisión real de interfaz: citas abiertas, abstención de credenciales, conflicto documental, traza, solicitud confirmada y alerta de evidencia. Preparar dejó cero solicitudes en C-011; confirmar produjo una solicitud y un evento, conservando el estado original. Idempotencia adicional comprobada por API.
- **D1–D8 y versión:** guion operativo trazado a los ocho resultados de la rúbrica P2 en `docs/guion-demostracion-v3.md`. La etiqueta técnica `v3.0` identifica el cierre seleccionado y no representa aprobación docente ni preparación productiva.

## Pendiente que no se sustituye por comprobaciones técnicas

1. **CORROBORAR ESTO: revisión humana independiente.** Los juicios de la muestra son técnicos y no humanos. El paquete `docs/paquete-revision-humana.md` contiene respuestas y fuentes; `evaluation/cierre_v3_20261107/muestra_humana_ejecucion06.csv` deja vacíos los juicios, fecha y revisor. Completar una revisión real, medir acuerdos por dimensión y conservar discrepancias si aparecen. La aprobación del golden no aprueba automáticamente las respuestas generadas.
2. **CORROBORAR ESTO: generación y ensayo integral.** El servicio Bonsai no estaba disponible y el usuario indicó continuar solo con lo que no lo requiere. No se reanudaron descargas. Falta repetir las consultas generadas, el cliente gráfico elegido y una pregunta sorpresa de otra persona. La evidencia histórica no se presenta como una nueva ejecución.
3. **CORROBORAR ESTO: corrección de E2.** No se encontró un documento identificado como retroalimentación oficial del docente. Las actas de usabilidad son retroalimentación de participantes, no corrección académica.
4. **CORROBORAR ESTO: instrucciones docentes adicionales.** El PDF nombra D1–D8 y v3.0 y enumera los resultados de la demo, pero no desarrolla otro guion numerado. El mapeo adoptado se declara como del equipo. No se inventa una confirmación docente; contrastar cualquier aclaración posterior.
5. **CORROBORAR ESTO: presentación y entrega.** Completar responsabilidades reales, PPT y revisión del PDF final dentro de los límites de páginas; ensayar 15 minutos con participación del equipo.

## Evidencia

La carpeta `evaluation/cierre_v3_20261107/` conserva pruebas, huellas, recuperación, cliente externo, consultas de API, observaciones de interfaz, revisión técnica, concordancia y aprobación del cliente. Las bases, claves y el entorno temporal no se distribuyen como fuentes del kit. Las ejecuciones previas permanecen con su contexto histórico.
