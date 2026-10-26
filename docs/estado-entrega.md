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

`python -m mira.cli evaluar` produce métricas de recuperación por fragmento y dos
configuraciones de tamaño máximo. Con este corpus de secciones breves, 900 y
1800 caracteres producen los mismos 35 fragmentos y ambos recuperan los 18
fragmentos esperados entre los seis resultados. Ese experimento no demuestra
superioridad de una configuración: se mantiene el límite de 1800 y la separación
por secciones por trazabilidad. Debe ampliarse la comparación si crece el corpus.

El primer control encontró un fallo de metadatos: una columna «Código» del cuerpo
de CAT-SEN reemplazaba el código del encabezado. Se corrigió el parser para leer
solo el encabezado y se añadió una prueba de regresión. El golden set no cambió.

## Pendiente antes de entregar

1. Validación de las respuestas esperadas por el representante del cliente.
2. Incorporar los documentos pertinentes de MIRA v1.4 y las referencias del equipo.
3. Ejecutar y revisar la evaluación completa de generación en el equipo de la demo.
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
