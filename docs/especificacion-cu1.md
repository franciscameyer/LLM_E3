# Especificación verificable del CU-1

Estado: implementación local de demostración; aceptación del cliente pendiente.
Fuentes: enunciado Entrega 3 §§3.1–3.3, 4–7 y rúbrica C2; kit CU-1 original.
Los identificadores siguientes son del proyecto, no identificadores del docente.

## Alcance y justificación

El operador necesita explicar una derivación sin sustituir a la persona que decide.
CU-1 permite contrastar reglas documentales con señales y datos de casos de
aseguradora, clínica y banco ficticios. El conflicto MAN-REV v1 §1 (80) frente
a POL-DEC v2 §2 (referencia 85) exige mostrar ambas fuentes vigentes. CU-001
añade una discrepancia: la plataforma reporta 90 sin acreditar dos supervisores
según POL-DEC v2 §5. No se resuelve silenciosamente ninguna de esas contradicciones.

## Necesidades y componente responsable

| Necesidad | Responsable | Razón |
| --- | --- | --- |
| Explicar señales, mínimos y procedimiento | RAG, publicado por MCP | Son reglas versionadas, no valores del caso |
| Consultar puntaje, evidencias y solicitudes de C-012 | Herramientas MCP y SQLite | Son datos vivos autorizados; recuperarlos de documentos no acredita su estado |
| Explicar por qué se derivó C-012 | RAG + MCP + modelo | Debe conectar la regla con los hechos consultados y advertir discrepancias |
| Preparar antecedentes | MCP de escritura de propuesta | Persiste un borrador, sin solicitud ni cambio del caso |
| Registrar la solicitud | Confirmación humana + MCP transaccional | Produce efecto; el modelo carece de la autorización de confirmación |
| Aprobar/rechazar, inventar pesos o resolver precedencia | Fuera de alcance | Lo primero es decisión humana; lo demás carece de evidencia o autoridad |

## Flujo principal

1. La persona inicia sesión con un usuario ficticio del kit.
2. Selecciona un caso de su organización; la API consulta su ficha por MCP y muestra traza.
3. Pregunta por la derivación. Se recuperan reglas y el modelo consulta los datos necesarios mediante herramientas MCP.
4. Se muestra evidencia o conflicto, con citas abiertas a fuente, sección y versión y trazas de las llamadas.
5. Si la persona pide antecedentes, el servidor valida rol, organización, estado y límite, y guarda una propuesta por diez minutos.
6. La persona revisa documentos/motivo y confirma expresamente en la interfaz.
7. El backend firma una autorización de confirmación de 30 segundos. MCP revalida y registra solicitud, evento y aviso simulado en una transacción.
8. La interfaz muestra ID de solicitud, nuevo estado y traza. Una repetición válida no duplica el efecto.

## Alternativas

| Condición | Resultado esperado |
| --- | --- |
| Pesos numéricos no documentados | Abstención explícita; no inventar porcentajes |
| Manual 80 frente a política 85 | Ambas fuentes, condiciones y discrepancia; sin elegir precedencia |
| Norma derogada | Usar vigente; búsqueda histórica solo para comparación identificada |
| C-020 con U-01, o ficha individual con U-03 | Error de permisos; no presentar datos inventados |
| C-016 con U-01 | Bloquear tercera solicitud, citando PRO-ANT §4 |
| Caso aprobado automáticamente | Bloquear solicitud según PRO-ANT §4 |
| Propuesta cancelada, vencida, de otra sesión o firma inválida | No escribir solicitud ni evento |
| Señal ausente en C-018 | Informar falta; no asumir cumplimiento del mínimo |
| E-007 de C-014 | Aislar instrucción conocida, conservar original y no aprobar |
| Modelo caído, formato o cita inválidos | Error explícito; retener respuesta no verificable |

## Requisitos y aceptación técnica

Los criterios son verificables por pruebas existentes; no constituyen aceptación del cliente.

| ID | Requisito y fuente | Criterio de aceptación / evidencia |
| --- | --- | --- |
| RF-01 | Explicar sin decidir; PR-1 | No ofrecer herramienta de aprobación ni atribuir aprobación al agente; `test_agente_no_expone_herramienta_de_confirmacion` |
| RF-02 | Citar fragmento, versión y sección; PR-2 | Retener IDs no recibidos; `test_agente_rechaza_citas_inventadas`; fidelidad semántica evaluada aparte |
| RF-03 | Abstenerse ante falta de evidencia; PR-3 | A01–A04 del golden; prohibir respuesta inventada ante caída del modelo |
| RF-04 | Mostrar conflicto sin elegir; PR-4 | Recuperar ambas fuentes; `test_conflicto_preserva_ambas_fuentes` y revisión semántica C01/C02 |
| RF-05 | Datos vivos por MCP visible; PR-5 | Sin ficha autorizada en esa consulta no mostrar el caso; `test_agente_se_abstiene_si_no_consulto_el_caso` |
| RF-06 | Confirmación explícita; PR-6 | Preparar no agrega solicitud; firma vinculada a acción/sesión; pruebas de preparación, caducidad e idempotencia |
| RF-07 | Aislar rol y organización; PR-7 | U-01 no ve C-020; U-03 no ve fichas; prueba de datos ajenos |
| RF-08 | Respetar límites; PRO-ANT §4 v1 | U-01 no registra tercera solicitud en C-016; supervisor sí puede prepararla |
| RF-09 | Conservar originales; enunciado §3.2 | Verificación Excel y triggers de UPDATE/DELETE; eventos anexos para el estado actual |
| RF-10 | Mantener vigencia; §4 y §7.1 | Filtrar derogadas por defecto; pruebas de metadatos y recuperación histórica |
| RNF-01 | Servidor propio y SQL parametrizado; §5 | Cliente STDIO real y argumento SQL tratado como dato |
| RNF-02 | Interfaz española y errores claros; §6 | Estados evidencia/abstención/conflicto y mensajes de proveedor; comprobación visual final del equipo pendiente |
| RNF-03 | Indexación separada y reproducible; §6.2 | `preparar` y `buscar`; comparación que exige el mismo contenido esperado |
| RNF-04 | Revalidar en transacción; §5 y PR-6 | Dos confirmaciones concurrentes no eluden el límite |

La corrección de montos y el recálculo se explican documentalmente, pero no se
implementan como herramientas en este CU. Tampoco existe callback externo real.
