# Guion operativo de demostración de la versión v3.0

Equipo: Francisca Meyer, Lukas Scheel y Sebastian Rodriguez. Representante del cliente: Francisca Meyer.

La rúbrica P2 enumera ocho resultados visibles: cita abierta, abstención, conflicto, traza, efecto verificado, riesgo contenido, cliente externo y pregunta no prevista. Este documento los organiza como D1–D8 en ese orden. El PDF no desarrolla un guion numerado adicional; el mapeo es una definición operativa del equipo basada en esos resultados, no una confirmación del docente sobre un orden obligatorio.

`v3.0` identifica la versión técnica de la Entrega 3 mediante etiqueta Git. No equivale a aceptación docente, validación de producción ni certificación de resultados aún pendientes. El código funcional de referencia es `6e86c44`; el commit de cierre incorpora el informe y la evidencia de sus verificaciones.

| Paso | Acción para mostrar en vivo | Resultado exigible | Ensayo sin Bonsai del 07-11 |
| --- | --- | --- | --- |
| D1: cita abierta | U-01, buscar el conflicto 80/85 en «Solo documentos» y abrir MAN-REV §1 y POL-DEC v2 §2. | Texto completo, fuente, sección, versión y vigencia visibles. | Comprobado en interfaz y API. No representa respuesta generada. |
| D2: abstención | Preguntar por la contraseña del administrador. | Abstención sin revelar secretos ni inventar recuperación; traza de búsqueda. | Ruta controlada comprobada sin generación. Para mostrar falta de evidencia documental general, repetir la pregunta de pesos con Bonsai. |
| D3: conflicto | Preguntar por manual 80 frente a política 85. | Ambas fuentes y ausencia de precedencia inventada. | Recuperación y estado de conflicto comprobados en interfaz. Redacción generada: disponible en ejecución 06, pendiente de reensayo actual. |
| D4: traza | Abrir la pestaña MCP y expandir una llamada. | Nombre, argumentos, resultado y fecha; autorización de confirmación omitida. | Comprobado con la confirmación de C-011. |
| D5: efecto confirmado | C-011: preparar; verificar que no hay solicitud; marcar confirmación y registrar. | Una nueva solicitud, cambio de estado por evento y traza. Repetir no duplica. | Preparación y confirmación en interfaz; idempotencia adicional por API en otro caso temporal. |
| D6: riesgo contenido | Revisar C-014, intentar C-031 como U-01 y una tercera solicitud de C-016. | Alerta de E-007 aislada; acceso ajeno y límite denegados. | Comprobado por API y suite; revisión directa no usa generación. |
| D7: cliente externo | Conectar por STDIO; listar herramientas, recurso y prompt; consulta autorizada y denegada. | Primitivas y permisos reales por MCP, sin SQL elegido por el cliente. | Cliente programático externo comprobado. CORROBORAR ESTO: ensayar el cliente gráfico que se mostrará al docente. |
| D8: pregunta no prevista | Otra persona del equipo o público formula una pregunta nueva dentro del alcance. | Respuesta respaldada, abstención o error honesto, con citas/trazas pertinentes. | Se comprobó una consulta exploratoria fuera del golden, sin generación. No se declara pregunta sorpresa de otra persona. CORROBORAR ESTO: ensayo con participante y Bonsai disponible. |

## Preparación del equipo

- Reservar una base nueva para la demo; no reutilizar el estado alterado por ensayos.
- Instalar dependencias y preparar datos según `docs/reproduccion.md`; verificar el modelo antes de presentar.
- Mantener separados resultados de ejecución 06, pruebas actuales y respuestas nuevas.
- Ensayar 15 minutos con exposición y demostración incluidas. Todos deben poder explicar un fallo y su corrección.
- El ensayo realizado sin Bonsai no acredita los pasos de generación. Las salidas históricas sirven como evidencia de evaluación, no sustituyen la demostración en vivo.

**CORROBORAR ESTO:** si el docente ha publicado instrucciones adicionales que definan D1–D8 o v3.0, contrastarlas con este guion. No se ha registrado una confirmación docente externa.
