# Estado de la implementación y de la entrega académica

## Implementado

- CU-1 con frontend web español, API, modelo local y servidor MCP propio por STDIO.
- Importación de las siete tablas y preservación de las filas originales.
- Recuperación documental BM25, metadatos, citas por fragmento, vigencia e inventario.
- Caso y señales desde MCP; aislamiento por organización y rol.
- Preparación y confirmación de solicitudes; límites revalidados en transacción,
  evento de estado, idempotencia y auditoría visible.
- Errores de proveedor explícitos; contexto acotado y control estructural de citas.
- Conflicto entre fuentes vigente declarado; discrepancia de umbral visible.
- Tratamiento del intento conocido de manipulación, más controles de permisos que
  no dependen de que el modelo reconozca la instrucción maliciosa.
- Golden set de 20 preguntas (12 con respuesta, 4 sin respuesta, 2 conflictos,
  2 versiones) guardado en el commit 089b2fb antes del pipeline.

## Evidencia de evaluación

Las pruebas automatizadas y sus resultados se obtienen con `python -m pytest -q`.
Cubren integridad del Excel importado, metadatos, vigencia, conflictos, roles,
organizaciones, instrucciones en evidencia, SQL parametrizado, firma/caducidad,
confirmaciones concurrentes, idempotencia, MCP externo, CSRF y errores del modelo.

La versión verificada pasa **23 pruebas**. Se conservaron dos ejecuciones de las
20 preguntas en `evaluation/ejecucion_01/` y `evaluation/ejecucion_02/`.
La segunda registra 20 respuestas sin error de servicio o de contrato, abstención
en 4/4 preguntas sin respuesta y 0/16 abstenciones en preguntas con respuesta.
Los dos conflictos y las dos preguntas de versiones incluyen los fragmentos
esperados en la comprobación estructural. Esto no acredita fidelidad semántica.
El tiempo medio fue 9,96 segundos, en secuencia y con el modelo ya cargado.

`python -m mira.cli evaluar` produce métricas de recuperación por fragmento y dos
configuraciones de tamaño máximo. Con este corpus de secciones breves, 900 y
1800 caracteres producen los mismos 35 fragmentos y ambos recuperan los 18
fragmentos esperados entre los seis resultados. Ese experimento no demuestra
superioridad de una configuración: se mantiene el límite de 1800 y la separación
por secciones por trazabilidad. Debe ampliarse la comparación si crece el corpus.

El primer control encontró un fallo de metadatos: una columna «Código» del cuerpo
de CAT-SEN reemplazaba el código del encabezado. Se corrigió el parser para leer
solo el encabezado y se añadió una prueba de regresión. El golden set no cambió.

La primera ejecución completa también mostró un fallo de generación en R10:
Bonsai añadió a una respuesta sobre roles la aprobación desde 80 de MAN-REV,
sin advertir la discrepancia vigente. Se corrigió el orden de relevancia, se
incluyó la contraparte de una fuente en conflicto como complemento del contexto
y se validó el conflicto por las fuentes citadas, además del tema de la pregunta.
La segunda ejecución de R10 responde solo con PRO-ANT §4 v1. La observación y
la regresión se conservaron; el golden set permaneció igual.

Una paráfrasis fuera del golden set sobre señales y umbrales de C-012 produjo
una cita no recibida en una prueba de interfaz: el control retuvo la respuesta.
Un reintento técnico de la misma formulación devolvió referencias válidas y
explicó el conflicto y el historial incompleto. Esto evidencia variabilidad
residual: las 20 preguntas no prueban el comportamiento en todas las consultas.
No se relajó el control de citas para aceptar la respuesta retenida.

## Pendiente antes de entregar

1. Validación de las respuestas esperadas por el representante del cliente.
2. Incorporar los documentos pertinentes de MIRA v1.4 y las referencias del equipo.
3. Revisar humanamente la evaluación completa de generación ejecutada y repetirla
   si el equipo cambia modelo, corpus o configuración antes de la demo.
   Precisión de cita y fidelidad requieren juicio del contenido. El evaluador
   genera una hoja CSV de revisión y deja esas métricas sin valor hasta medirlas.
4. Preparar el informe PDF con las extensiones de la pauta y una presentación PPT
   coherente con los resultados finales. No se han generado documentos que afirmen
   una validación, una métrica de generación o una aprobación inexistentes.
5. Acordar con el docente el alcance de D1–D8/v3.0, que la pauta referencia sin detallar.

## Guion propuesto para la demo

1. Entrar como U-01 y explicar C-012 abriendo ficha, cita y traza.
2. Preguntar por los pesos del puntaje y mostrar la ausencia de evidencia.
3. Contrastar los umbrales del manual y la política, abriendo ambas fuentes vigentes.
4. Mostrar el cambio de regla de fraude entre POL-DEC v1 y v2.
5. Intentar preparar una tercera solicitud en C-016 como operador y ver el rechazo.
6. Preparar en C-011, revisar, confirmar y verificar solicitud/evento en una traza.
7. Mostrar E-007 de C-014 y el contenido aislado, sin aprobación por el asistente.
8. Cambiar a U-04 y comprobar la organización; conectar el servidor desde VS Code
   y probar una pregunta adicional que el equipo no haya memorizado.

Este guion es una propuesta del proyecto, no una sustitución de criterios faltantes.
