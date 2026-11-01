# Contratos MCP del proyecto

Implementación: `mira/mcp_server.py`, `mira/store.py`, `mira/security.py`.
Transporte STDIO con FastMCP; cliente externo de prueba en `.vscode/mcp.json`.
El proceso recibe identidad firmada por entorno, nunca por argumentos elegidos por el modelo.
Esto es identidad local de demostración, no autenticación remota de producción.

## Envoltorio y errores

Éxito: `{ok: true, datos: <salida de la tabla>, traza: {...}}`.
Fallo de negocio: `{ok: false, error: "mensaje comprensible", traza: {...}}`.
Traza: `id`, `fecha`, `usuario`, `herramienta`, `argumentos`, `ok`, `resultado`.
Las autorizaciones de confirmación se omiten de argumentos auditados.
La identidad se verifica antes del envoltorio: una identidad inválida produce error
del protocolo sin traza de negocio atribuida a una persona no autenticada.
Errores de validación de esquema también pueden proceder del protocolo MCP.

Todas las herramientas leen/escriben auditoría. `readOnlyHint` significa sin efectos
de negocio, no ausencia de escrituras de auditoría. Solo las primeras cinco herramientas
se ofrecen al modelo. Las demás se usan desde la aplicación o clientes de desarrollo.

## Herramientas

| Nombre | Entrada | Salida `datos` | Permisos, errores y efecto |
| --- | --- | --- | --- |
| `buscar_reglas` | `pregunta: str`, `k: int=6`, `historico: bool=false` | `fragmentos[]`, `complementarios_conflicto[]`, `conflictos[]`, `advertencia` | Usuario identificado; consulta no vacía, k entre 1 y 12. Solo vigentes por defecto. No contiene datos vivos. El filtro de conflicto puede devolver al menos dos fragmentos incluso con k=1; las evaluaciones fijan k=6. Sin efecto de negocio |
| `listar_casos` | Sin argumentos | Lista de `caso_id,tipo_proceso,puntaje,motivo_derivacion,vence_el,estado` | Operador/supervisor; solo organización conectada. Estado considera eventos anexos |
| `consultar_caso` | `caso_id: str` | `caso,organizacion,cambios_umbral,senales,evidencias,solicitudes,discrepancias,reglas_relevantes,conflictos_documentales` | Operador/supervisor, misma organización; caso ajeno/inexistente produce el mismo mensaje. Las reglas relevantes provienen de buscar el motivo registrado (k=3), sus complementos y las discrepancias. Conserva vigencia y conflictos. Aísla manipulación conocida; no altera original |
| `listar_senales` | `caso_id: str` | Filas de señales del caso | Primero verifica visibilidad del caso; SQL parametrizado |
| `preparar_solicitud` | `caso_id: str, documentos: str, motivo: str` | `accion_id,caso_id,documentos_solicitados,motivo,regla,regla_limites,requiere_confirmacion,vence_en_segundos,efecto` | Operador/supervisor, organización, estado y límite de PRO-ANT. Documentos 5–1000 caracteres tras trim; motivo 10–1500. Persiste propuesta por 600 s; no solicitud ni evento |
| `confirmar_solicitud` | `accion_id: str, autorizacion: str` | `solicitud_id,caso_id,estado,registrada_por,fecha,aviso_origen`; en repetición `repeticion_sin_efecto: true` | Firma propósito confirmación, usuario/sesión/acción y caducidad. Solo propuesta propia vigente. `BEGIN IMMEDIATE`, revalida límites; inserta solicitud, evento y aviso simulado atómicamente. Nunca expuesta al modelo. La repetición exige autorización válida |
| `ver_propuestas` | Sin argumentos | Lista de propuestas propias vigentes con `accion_id`, contenido y `vence` | Solo usuario y sesión conectados, pendientes y no vencidas; sin efecto de negocio |
| `cancelar_propuesta` | `accion_id: str` | `cancelada: true, accion_id` | Solo propuesta propia pendiente; si no está disponible, error. Cambia propuesta a cancelada; no caso ni solicitud |
| `ver_trazas` | Sin argumentos | Hasta 40 filas de auditoría propias, argumentos y resultados deserializados | Solo usuario/sesión conectados. La respuesta contiene el historial anterior a la traza de esta llamada |

## Fragmentos y primitivas adicionales

Cada fragmento contiene `id,codigo,version,estado,vigencia,desde,hasta,fuente,titulo,
origen,sha256,seccion,texto,texto_busqueda`; búsqueda añade `relevancia` cuando
proviene del ranking. Los fragmentos insertados por relación de conflicto pueden
no tener esa puntuación. `complementarios_conflicto` queda fuera de k.

Recurso `mira://corpus/inventario`: usuario identificado; texto JSON con documentos,
versiones, vigencia, origen, huella y tamaño aproximado en tokens; sin casos.
Prompt `revisar_caso(caso_id: str)`: guía textual para consultar caso y reglas,
declarar conflictos y abstenerse de decidir. No ejecuta consultas ni concede acceso;
la autorización se aplica en cada herramienta utilizada después.

Los esquemas efectivos de entrada/salida y las anotaciones se conservan en
`evaluation/cierre_tecnico/verificacion_mcp_parafrasis.json`, obtenidos desde un
cliente MCP real. Estos esquemas prevalecen ante cambios de implementación.
