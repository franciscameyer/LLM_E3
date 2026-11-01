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

La versión actual pasa **40 pruebas**. Se conservaron dos ejecuciones de las
20 preguntas en `evaluation/ejecucion_01/` y `evaluation/ejecucion_02/`.
La segunda registra 20 respuestas sin error de servicio o de contrato, abstención
en 4/4 preguntas sin respuesta y 0/16 abstenciones en preguntas con respuesta.
Los dos conflictos y las dos preguntas de versiones incluyen los fragmentos
esperados en la comprobación estructural. Esto no acredita fidelidad semántica.
El tiempo medio fue 9,96 segundos, en secuencia y con el modelo ya cargado.

La comparación ampliada `python -m mira.validation comparar --salida <archivo-nuevo>`
usa 300, 600, 900 y 1800 caracteres: produce 50, 36, 35 y 35 fragmentos. Exige
recuperar TODO el texto original esperado, no solo el ID :01. Recupera objetivos
completos en 10/18, 17/18, 18/18 y 18/18, respectivamente, dentro de k=6.
Se mantiene 1800 para preservar secciones/tablas y contratos existentes; empata
con 900. El método incluye la relación de conflicto existente y excluye complementos
fuera de k. Datos, denominadores y límites en `docs/reproduccion.md`.

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

## Cierre técnico del 2026-11-01

- Especificación del CU-1 con requisitos, fuentes, flujos y criterios verificables.
- Contratos MCP con entradas/salidas/permisos y mapa de riesgos, controles y pruebas.
- Comparación real de fragmentación y métricas recalculables sin modificar el golden.
- Lectura semántica de las 20 respuestas de la ejecución 02: el agente juzgó
  respaldadas 31/31 citas únicas por respuesta, fieles 20/20 respuestas y correcto
  el manejo de los cuatro casos de conflicto/vigencia. Es evaluación automatizada
  provisional; no validación del cliente ni revisión humana. Ver juicios por ID.
- Ocho consultas exploratorias con Bonsai y cliente MCP externo, en base temporal.
  La primera exploración detectó una abstención con afirmaciones no respaldadas
  sobre pesos y una denegación por rol que terminaba en error de cita. No se
  presentan esas consultas como ocho éxitos semánticos.
- Corrección: las denegaciones MCP por rol/organización se muestran directamente,
  sin reformulación del modelo; pruebas de regresión para ambos casos. Se refuerzan
  instrucciones para no añadir citas ajenas ni contenido de secciones no recibidas.
- Una repetición exploratoria conservada en `verificacion_posterior.json` mostró
  tres respuestas retenidas por IDs inválidos (P01/P06/P07). Se añadió un único
  reintento con la misma evidencia, sin tools y con validación completa posterior;
  un ID incorrecto nunca se acepta ni se corrige por semejanza. La cuarta ejecución
  conserva la evaluación completa de esa versión.
- La ejecución 04 terminó 20/20 sin errores de contrato/servicio, con abstención
  en 4/4 preguntas sin respuesta y 0/16 en las demás. La lectura semántica del
  agente es 19/20 fieles: A04 presupone canales de recuperación de credenciales
  no documentados, aunque no revela ninguna contraseña. C01/C02 no repiten la
  localización incorrecta observada en ejecución 03. No se atribuye causalidad
  garantizada a un cambio de prompt ni se infiere generalización de esta muestra.
- La repetición dirigida de P01/P06/P07 con el reintento obtuvo dos salidas
  estructuralmente aceptadas y mantuvo P07 retenida por citas inválidas. La revisión
  exploratoria advierte sobrecitación en P01 y lenguaje con apariencia de decisión
  en P06. Son límites técnicos medidos, no pendientes que deba aprobar el cliente.
  Ver `evaluation/cierre_tecnico/analisis_exploratorio.json`.
- Reejecución completa del golden en `evaluation/ejecucion_03/`; no reutilizar
  automáticamente las métricas semánticas de la ejecución 02 para nuevas respuestas.
  Las 20 preguntas terminaron sin error de servicio/contrato; abstención correcta
  4/4 y sin abstenciones en 16 con respuesta. La nueva lectura del agente marca
  dos fallos de fidelidad (C01/C02): ubican ambiguamente la configuración efectiva
  en la sección 5 de la política. Las reglas citadas son correctas, pero el dato vivo
  debe provenir de MCP. No se declara la generación perfecta ni se oculta esa regresión.
- Instalación en venv nuevo y copia de fuentes sin entorno/datos previos; evidencia
  inicial en `evaluation/cierre_tecnico/instalacion_limpia.json` y versión final en
  `instalacion_final.json`. No acredita otro equipo físico.
- Lanzadores unificados y rutas de modelo/CUDA configurables por `.env`.

## Pendiente de validación externa y del equipo

1. Validación de las respuestas esperadas por el representante del cliente.
2. Docente: aclarar D1–D8 y qué exige la etiqueta v3.0. No se creó una etiqueta final.
3. Equipo humano: revisar una muestra independiente y medir concordancia con el
   evaluador automático; continuar revisión si hay desacuerdos. Planilla y procedimiento
   preparados. Repetir evaluación si cambia corpus, modelo o comportamiento.
4. Equipo: contrastar MIRA v1.4/entrevistas y retroalimentación cuando aporte esos
   antecedentes; no es obligatorio añadirlos al corpus del kit.
5. Equipo: ensayo visual en el hardware definitivo, cliente externo y defensa individual.
6. Informe/PPT: fuera del alcance solicitado al agente; siguen siendo entregables
   del curso y no se han generado.

Responsables, evidencia requerida y límites en `docs/validaciones-pendientes.md`.

## Corrección posterior de P07 y A04

- P07: la pregunta por CRUCE_MONTO ausente recuperaba mínimos pero no POL-DEC v2
  §6. Consultar la ficha ahora recupera también reglas desde el motivo registrado;
  el contexto prioriza fuentes recientes. Los fragmentos realmente mostrados reciben
  referencias cortas F1/F2, resueltas de forma exacta a los IDs originales. No se
  normalizan por semejanza ni se aceptan fuentes recuperadas pero no mostradas.
- A04: una petición directa de credenciales produce abstención controlada después
  de la búsqueda auditada, sin invocar al LLM ni inventar canales de recuperación.
- Los dos casos pasaron tres repeticiones cada uno con el código final: P07 explica
  la señal ausente con POL-DEC v2 §6 sin errores ni reintentos; A04 no inventa datos.
- Se conserva el intento intermedio donde enriquecer evidencia sin referencias
  cortas todavía fallaba. La revisión dirigida registra sobrecitación documental
  de hechos de la ficha en P07; no la cuenta como precisión de cita perfecta.
- `evaluation/ejecucion_05/` guarda la evaluación completa posterior. Los resultados
  y revisiones de ejecuciones anteriores mantienen su contexto histórico.
- Las 20 preguntas terminaron sin error de servicio/contrato, con abstención 4/4
  y ninguna abstención injustificada en las otras 16. La lectura del agente marca
  20/20 fieles en este golden, incluido A04 corregido. Es evaluación automatizada
  provisional, no revisión humana ni validación del representante del cliente.
- Las validaciones del cliente, del docente y la muestra humana siguen pendientes.

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
