# Índice de evidencia técnica

Fecha: 2026-11-01. Datos ficticios del kit. No es el informe académico.

| Archivo | Qué acredita y qué no |
| --- | --- |
| `inventario_corpus.json` | Fuente, título, versión, vigencia, huella y tokens aproximados de los seis documentos originales |
| `comparacion_fragmentacion.json` | Cuatro límites, contenido completo esperado, resultados por pregunta, firmas y contexto medio. No evalúa fidelidad |
| `revision_semantica_agente.json` / `metricas_semanticas_agente.json` | Lectura automatizada de la ejecución 02, vinculada por SHA-256; no revisión humana |
| `muestra_humana.csv` | Planilla vacía para muestra de ejecución 02; no acredita aprobación |
| `verificacion_mcp_parafrasis.json` | Contratos obtenidos por MCP, denegaciones, propuesta cancelada y ocho respuestas exploratorias antes de las correcciones |
| `verificacion_posterior.json` | Ocho consultas tras la denegación determinista; incluye tres respuestas retenidas por citas inválidas. Se conserva como evidencia de fallo |
| `verificacion_reintento.json` | Repetición dirigida de las consultas P01/P06/P07 con el reintento limitado; no equivale a una nueva muestra independiente |
| `analisis_exploratorio.json` | Sobrecitación, apariencia de decisión y una respuesta retenida tras reintento: límites técnicos que no se ocultan como simples aprobaciones pendientes |
| `instalacion_limpia.json` / `pruebas_instalacion_limpia.xml` | Primera copia limpia y 29 pruebas |
| `instalacion_final.json` / `pruebas_instalacion_final.xml` | Copia final y dependencias en venv nuevo, pruebas y smoke HTTP/MCP; mismo equipo físico |
| `pruebas.xml` | Suite de la versión final en el entorno de desarrollo |
| `runtime_modelo.json` | SHA-256 real del GGUF y servidor locales, alias, plataforma y parámetros; no distribuye pesos |
| `resumen.json` | Índice de resultados actuales y validaciones pendientes; remite a evidencia por archivo |

Las ejecuciones completas 01, 02, 03 y 04 quedan en carpetas separadas.
La revisión semántica de cada una se aplica solo a su archivo y hash, nunca se
traspasan puntuaciones a respuestas nuevas sin leerlas. La muestra humana de la
versión actual se prepara junto a la ejecución 04; la ejecución 03 conserva sus
dos fallos de fidelidad en C01/C02.

No se ha registrado validación del representante del cliente, respuesta del
docente sobre D1–D8/v3.0 ni concordancia humana. Ver `docs/validaciones-pendientes.md`.
