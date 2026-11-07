# Evidencia del cierre técnico de v3.0

Fecha local: 7 de noviembre de 2026. Código funcional verificado: `6e86c44`.

| Archivo | Evidencia y alcance |
| --- | --- |
| `pruebas.xml` | 47 pruebas aprobadas, cero errores, fallos u omisiones. Incluye proveedor simulado; no es evaluación de Bonsai. |
| `fragmentacion.json` | Comparación actual de 300, 600, 900 y 1800 caracteres; a 1800 recupera 18/18 objetivos y 16/16 preguntas. |
| `mcp_externo.json` | Cliente STDIO real: herramientas, recurso, prompt, denegaciones, límite y cancelación de propuesta en base temporal. |
| `ensayo_api_sin_bonsai.json` | Nueve escenarios reales de API con rutas que no invocan generación. |
| `ensayo_interfaz.json` | Observaciones de la interfaz real: citas abiertas, abstención controlada, conflicto documental, confirmación, traza y alerta. |
| `antes_confirmacion.json` y `despues_confirmacion.json` | C-011 pasó de cero solicitudes y una propuesta a una solicitud y un evento; conserva estado original de importación. |
| `revision_tecnica_muestra.json` | Nueva lectura técnica de ocho respuestas y fragmentos de ejecución 06, con huellas. No es revisión humana ni nueva generación. |
| `concordancia_tecnica.json` | 14/14 citas respaldadas; acuerdos técnicos 8/8 en fidelidad y cantidad de citas y 3/3 en conflicto/vigencia; no discrepancias en la muestra. |
| `muestra_humana_ejecucion06.csv` | Campos humanos sin completar y ejecución identificada por hash. No se rellenan en nombre de una persona. |
| `aprobacion_cliente.json` | Aprobación de las veinte preguntas y expectativas por Francisca Meyer, comunicada explícitamente en el chat; sin firma digital. |
| `resumen.json` | Identidad de fuentes, entorno y límites del cierre. |

`preparar_revision.py` conserva el procedimiento y juicios de la revisión técnica. `ensayo_api.py` reproduce los escenarios contra una demo nueva servida en localhost:8765; produce escrituras solo en esa base de ensayo. No usarlo sobre una base con acciones que se desee preservar.

Las evidencias no se sobrescriben. Para repetir, utilizar otra carpeta de salida y otra base temporal. El golden original permanece sin modificaciones. `docs/paquete-revision-humana.md` reúne las respuestas y fuentes para el contraste humano pendiente. La generación con Bonsai y la pregunta sorpresa con participantes no se ejecutaron en este cierre, siguiendo la indicación del usuario de continuar sin el modelo.
