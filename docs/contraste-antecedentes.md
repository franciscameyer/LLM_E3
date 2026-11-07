# Contraste de antecedentes para la Entrega 3

Fecha de revisión: 7 de noviembre de 2026. Equipo: Francisca Meyer, Lukas Scheel y Sebastian Rodriguez. Representante del cliente para E3: Francisca Meyer, según identificación proporcionada por el equipo. Los nombres de las entrevistas pertenecen al levantamiento del caso y no identifican a la representante académica de E3.

## Fuentes efectivamente leídas

- Descripción completa: `T:/Desktop/UV_ICI-1/2026/2SEM/LLM/MIRA-descripcion-proyecto.docx`, capítulo 7. SHA-256: `904c977f1be7215352805e9d19cd96affbaa5c6fd1499aff09438b80b623d9de`; coincide con el original identificado por los extractos del repositorio.
- Informe E2: `T:/Desktop/UV_ICI-1/2026/2SEM/LLM/E2/Software-asistido-por-LLMs/docs/informe-entrega.md`, introducción, selección F4/F1, decisiones, evaluación y comparación con E1.
- Registro de usabilidad E2: `T:/Desktop/UV_ICI-1/2026/2SEM/LLM/E2/Software-asistido-por-LLMs/docs/qa/usabilidad-px05.md`.
- Corpus y reglas originales del kit CU-1 y los cuatro extractos MIRA-DESC ya incorporados.

Los antecedentes se usan para este contraste; no se añadieron entrevistas ni reglas de E2 al índice de recuperación. No se ha encontrado un documento identificado como corrección oficial del docente de E2. La evaluación de usabilidad de E2 no se presenta como esa corrección.

## Hallazgos y tratamiento

| Fuente y localizador | Necesidad o discrepancia | Tratamiento en CU-1 | Límite |
| --- | --- | --- | --- |
| ENT2, Camila Ordóñez, 00:13:05 | 85 y 60 son referencias de demostración; los valores requieren calibración por proceso. | Se distingue valor de referencia, configuración reportada y validez del cambio. | No se presenta un umbral universal ni se calibra riesgo con el kit ficticio. |
| ENT4, Francisca Leiva, 00:11:06, frente a ENT6, Daniela Cortés, 00:21:16 | Operaciones propone iniciar sobre 90 y cambiar unilateralmente; cumplimiento exige doble aprobación. | Se conserva el valor reportado 90 de ORG-01 y se advierte que CU-001 no acredita dos aprobaciones según POL-DEC v2 §5. | La entrevista no autoriza a cambiar la base ni resuelve por sí sola la contradicción. |
| ENT4, 00:16:26; ENT5, Marco Peñailillo, 00:02:46 y 00:05:07 | Evidencia y motivo de derivación en una misma pantalla; el puntaje aislado no explica el caso. | Ficha, señales, evidencia, citas y trazas en la interfaz. | La demo trabaja con texto extraído del kit, sin visor multimodal completo. |
| ENT5, 00:12:45 y 00:15:16 | Riesgo de confirmar por inercia y sesgo de mostrar primero el puntaje. | Separación de propuesta y confirmación, sin aprobación automática desde el asistente. | El puntaje sigue visible en la ficha; no se declara implementada la preferencia de ocultarlo hasta revisar evidencia. |
| ENT6, 00:04:06 | Rechazo automático incompatible con la necesidad expresada en la entrevista. | Ninguna herramienta aprueba o rechaza casos; POL-DEC v2 exige intervención humana para rechazo. | No se atribuye a esta revisión una conclusión jurídica. |
| ENT3, Sebastián Alarcón, 00:05:47 | Reconstruir un registro no equivale a repetir y obtener idéntica salida. | Se conservan respuestas, versiones y huellas de cada ejecución; no se transfieren juicios a respuestas nuevas. | No se garantiza determinismo de la generación. |
| MIRA §2.11 frente a ENT6, 00:07:26 | Documento: 90 días; cumplimiento: cinco años y a veces diez. | Se identifica la discrepancia en el análisis de antecedentes. | No se implementa borrado automático ni se elige un plazo. Las entrevistas no forman parte del corpus consultable actual. |
| ENT7, Hugo Marambio, 00:01:06 y 00:03:46 | El sistema de origen usa intercambio de archivos, no retorno en línea al core. | Aviso al origen declarado como cola simulada. | No existe integración real por archivos ni callback. |
| ENT9, Tomás Berríos, 00:12:21 | Acceso de soporte requiere autorización y registro. | CU-1 restringe usuarios por rol y organización y registra llamadas. | No implementa acceso productivo de soporte ni federación de identidades. |
| Informe E2, selección F4/F1 y DEC-E2-01/02/04/07 | Umbral 90 y mínimos concretos eran decisiones del piloto; se distinguían meta interna y compromiso. | E3 usa las reglas y tablas de su propio kit, sin importar silenciosamente políticas particulares de E2. | La aceptación de E2 no valida el golden de E3. |
| Actas de usabilidad E2, 03 y 04 de octubre | Una sesión necesitó ayuda para ubicar botones y entender secciones. | Se ensayan acceso a citas, trazas y confirmación de forma explícita. | No acredita una nueva prueba de usabilidad con personas ni una mejora medida. |

## Estado de cierre

Contraste documental e identificación de discrepancias: realizados. **CORROBORAR ESTO:** aportar y contrastar la corrección oficial de E2 si existe, confirmar decisiones de producto aún abiertas y completar el ensayo humano de defensa. Ninguna aprobación previa se traslada a E3.
