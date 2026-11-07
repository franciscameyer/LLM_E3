# Corroboración del informe de v3.0

Pruebas del 7 de noviembre de 2026 sobre el código de la etiqueta publicada `v3.0` (`c555046`). El último cambio funcional es `6e86c44`. Las bases de ensayo se prepararon por separado desde el Excel del kit. `entorno.json` identifica la configuración, el motor y los pesos por huella.

| Evidencia | Alcance |
| --- | --- |
| `golden/` | Recuperación y 20 respuestas con Bonsai. Se conservan citas, trazas, tiempos y huellas. |
| `revision_semantica_codex.json` y `metricas_semanticas_codex.json` | Juicio técnico sobre la nueva ejecución. 32/32 citas respaldadas, 18/20 respuestas fieles. A01 y C01 añadieron afirmaciones sin respaldo. |
| `muestra_humana.csv` | Ocho filas dirigidas al contraste humano. La huella identifica la ejecución y los juicios permanecen vacíos. |
| `pruebas.xml` | 47 pruebas, sin fallos, errores u omisiones. |
| `regresiones/resultados.json` | Tres repeticiones de P07 y tres de A04 con control estructural aprobado. |
| `mcp_y_parafrasis.json` | Primitivas, permisos, cancelación y ocho preguntas de exploración. P06 fue retenida por una fuente omitida. |
| `vscode_mcp.json` | Inicio por STDIO, nueve herramientas descubiertas y lectura del inventario en VS Code. |
| `ensayo_web_bonsai.json` | La repetición web de P06 dio evidencia con una cita abierta y trazas. Se observó información adicional ajena a la consulta. |
| `contrastes_y_d8.json` | Cinco contrastes documentales y dos preguntas nuevas de Codex. Las siete cumplieron el control estructural. |

La revisión de contenido del golden corresponde a Codex. La hoja humana apunta a las respuestas nuevas. Las dos preguntas de D8 fueron propuestas por Codex a petición del usuario y quedan como ensayo exploratorio. El cierre previo de la etiqueta se conserva en `../cierre_v3_20261107/`.

Las huellas entre estos archivos usan bytes con saltos de línea LF, fijados por `.gitattributes`. Las huellas del entorno de ejecución se conservan tal como se registraron durante las pruebas.
