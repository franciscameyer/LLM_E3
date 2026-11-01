# Validaciones externas y cierre del equipo

Actualizado: 2026-11-01. Este archivo distingue tareas técnicas verificables de
decisiones que el agente no puede aprobar en nombre de otra persona.
No es el informe académico ni una presentación.

## Cliente: VC-01, pendiente

El representante del cliente debe validar las 20 preguntas, respuestas y fragmentos
esperados de `evaluation/golden.json`. El archivo original y su commit `089b2fb`
se conservan; ejecutar pruebas no equivale a validarlo.

Registrar persona/rol, fecha, versión y SHA-256 del golden, observaciones por ID y
aceptación o cambios solicitados. No completar estos datos sin respuesta real.
Si pide cambios, crear una versión nueva, conservar la anterior y evaluarla de nuevo.

## Docente: VD-01 y VD-02, pendientes

- VD-01: pedir el guion oficial D1–D8 o confirmar si acepta la propuesta técnica de
  `docs/reproduccion.md`. El PDF lo menciona en la rúbrica, pero no define cada paso.
- VD-02: confirmar qué representa v3.0 y cuándo debe etiquetarse. No se presenta
  este cierre como una versión final aprobada ni se crea una etiqueta v3.0 ficticia.

Solicitar respuesta concreta y guardar su fecha, texto o referencia y criterio acordado.
No requiere preguntar si BM25, un LLM local o elegir solo CU-1 están permitidos:
el enunciado deja libre el stack y exige un caso. Los documentos adicionales del
equipo son opcionales; los seis Markdown del kit CU-1 son obligatorios y están incluidos.

## Equipo: VE-01, revisión humana pendiente

La evaluación semántica del agente es un juicio automatizado, no aprobación del cliente.
El enunciado permite evaluador automático, pero exige muestra manual y concordancia.

1. Leer las respuestas y fragmentos de la ejecución indicada en cada archivo de revisión.
2. Completar `evaluation/ejecucion_04/muestra_humana.csv` para la versión actual;
   la muestra cubre R01, R08, A01, A02, A04, C01, C02 y V02 (8 de 20, todos los tipos
   y preguntas con fallos previos o actuales). Es muestra dirigida, no aleatoria ni
   una estimación estadística de todas las consultas posibles. Las muestras anteriores se conservan aparte.
3. Para ejecuciones posteriores, crear otra planilla referida explícitamente a su
   hash; no reutilizar juicios de la ejecución 02 sin leer las nuevas respuestas.
4. Contar citas respaldadas por ID único en cada respuesta; anotar fidelidad 0/1 y
   conflicto/vigencia 0/1 cuando corresponda. Registrar revisor, fecha y discrepancias.
5. Comparar contra la revisión del agente: informar acuerdos/juicios comparados
   por separado para fidelidad, cantidad de citas respaldadas y conflicto/vigencia.
   La comparación de cantidades es concordancia agregada por respuesta, no por cita
   individual. Resolver desacuerdos leyendo fuentes y conservar ambos juicios.

Una muestra sin completar no produce concordancia cero ni cien por ciento: queda
sin medir. No sustituirla por una segunda revisión del mismo agente.

La revisión automatizada de la ejecución 03 marca dos fallos de generación en
C01/C02: las respuestas presentan el conflicto, pero su frase final ubica el valor
configurado de una organización en la sección 5 de la política. Esa sección define
el procedimiento de cambio, no acredita un valor vivo: este debe venir de MCP.
Es una limitación de fidelidad residual, no una decisión pendiente del cliente.
Las instrucciones se reforzaron, pero no garantizan eliminar toda inferencia del LLM.
Debe mostrarse el resultado medido y revisar estas dos respuestas con el equipo.

En la ejecución 04 esas dos inferencias de C01/C02 no reaparecen. La revisión del
agente marca 19/20 respuestas fieles y observa A04 bajo un criterio conservador:
se abstiene correctamente de revelar contraseñas, pero presupone canales oficiales
de recuperación de credenciales de MIRA no documentados. La muestra debe contrastar
este juicio; no se afirma que tales canales existan ni que no existan. Las cifras
son provisionales y no prueban ausencia de fallos en consultas nuevas.

La exploración dirigida final mantiene P07 sin respuesta útil por citas inválidas
(retenidas incluso tras reintento). P01 muestra sobrecitación y P06 lenguaje que
puede aparentar una decisión. Esto requiere seguimiento técnico y revisión del
equipo, no una aprobación del cliente para darlo por solucionado. Conservar el
error honesto es preferible a presentar una salida como verificada sin respaldo;
no se desactivaron los controles para mejorar la cifra.

## Equipo: VE-02 y VE-03, pendientes

- VE-02: revisar MIRA v1.4, entrevistas y retroalimentación E1/E2 que no estaban en
  esta carpeta. Son antecedentes; no es obligatorio añadirlos al corpus. Si se añade
  material, declararlo en el inventario y repetir las evaluaciones afectadas.
- VE-03: ensayo visual en el equipo definitivo y cliente MCP externo elegido.
  La verificación programática de MCP no acredita por sí sola la operación de VS Code
  ni que todo el equipo domine la defensa técnica. Recorrer citas, trazas, escrituras
  confirmadas, rechazo, cliente externo y una pregunta no ensayada.

La fecha del enunciado es lunes 9 de noviembre de 2026, 14:00. Informe y PPT quedan
fuera de la tarea solicitada al agente; siguen siendo entregables académicos del equipo.
