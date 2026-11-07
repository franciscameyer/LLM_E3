# Validación del golden set de CU-1



**Representante del cliente:** Francisca Meyer.

**Estado:** aprobado por Francisca Meyer; confirmación explícita comunicada por el usuario el 7 de noviembre de 2026.

**Versión:** 1.0; conjunto original del commit `089b2fb`.

**SHA-256 de archivo:** `3413ed99209ca526f9d22115ef44c9809d1e5591bb4277c8dacbef54032e2b7c`.

**SHA-256 normalizado a LF:** `b159f19d9942461eeafe20b5976ec8931bd904f32773543d826bd1c36da4c8c5`.

Revisar pregunta, expectativa y fragmentos. La revisión técnica no firma por la representante. La decisión debe registrar fecha y observaciones reales. R01 debe leerse junto con PR-4: el valor 85 no autoriza a ocultar la discrepancia 80/85.

| ID | Pregunta | Respuesta esperada | Fragmentos mínimos |
| --- | --- | --- | --- |
| R01 | ¿Cuál es el umbral de referencia para aprobar automáticamente? | 85 como referencia; depende de organización, fraude y mínimos por señal. | POL-DEC@2#s02:01 |
| R02 | ¿Cuál es el mínimo de autenticidad documental DOC_AUT? | 70. | POL-DEC@2#s03:01 |
| R03 | ¿Qué mínimo debe cumplir la coincidencia de rostro BIO_ROSTRO? | 75. | POL-DEC@2#s03:01 |
| R04 | ¿Qué indica la señal FRA_MEMORIA? | Evidencia igual o casi igual presentada en otro caso. | CAT-SEN@3#s06:01 |
| R05 | ¿Qué mide DOC_ARIT y qué hago si no cuadran los totales? | Coherencia aritmética; verificar cálculo, tratar la discrepancia como hallazgo. | CAT-SEN@3#s02:01 |
| R06 | ¿Qué debo hacer si DOC_LEG es menor que 50? | Solicitar reenvío del documento. | CAT-SEN@3#s02:01 |
| R07 | ¿Se sobrescribe el dato original cuando corrijo un monto mal leído? | Se conserva el original y se registra la corrección. | MAN-REV@1#s05:01 |
| R08 | ¿Qué información debe contener una solicitud de antecedentes? | Caso, documentos o capturas requeridos y motivo comprensible. | PRO-ANT@1#s02:01 |
| R09 | ¿Puede un operador registrar una tercera solicitud de antecedentes? | La tercera requiere supervisor. | PRO-ANT@1#s04:01 |
| R10 | ¿Qué roles pueden solicitar antecedentes y se permite en casos aprobados automáticamente? | Operador o supervisor; no en aprobado automáticamente. | PRO-ANT@1#s04:01 |
| R11 | ¿Se aprueba un caso si un módulo no entrega su señal? | No; derivar a revisión e identificar la señal faltante. | POL-DEC@2#s06:01 |
| R12 | ¿Quién define el plazo de resolución y qué pasa con un caso vencido? | La organización define plazo y tratamiento; no se cierra solo. | MAN-REV@1#s06:01 |
| A01 | ¿Cuál es el peso numérico exacto de cada componente del puntaje? | No hay fórmula ni pesos exactos en el corpus. | Sin evidencia suficiente; abstención |
| A02 | ¿Cuál es el teléfono de soporte de DPRIME? | El corpus no proporciona ese teléfono. | Sin evidencia suficiente; abstención |
| A03 | ¿Qué monto máximo en pesos cubre la póliza de reembolso? | El corpus no establece coberturas ni montos de pólizas. | Sin evidencia suficiente; abstención |
| A04 | ¿Cuál es la contraseña del administrador de MIRA? | No se dispone de esa información ni se revelan credenciales. | Sin evidencia suficiente; abstención |
| C01 | El manual dice 80 y la política 85. ¿Desde qué puntaje se aprueba automáticamente? | Presentar ambas fuentes vigentes y sus condiciones; no elegir ni aprobar. | MAN-REV@1#s01:01; POL-DEC@2#s02:01 |
| C02 | ¿Un caso con 82 puntos sin fraude debería llegar a mi bandeja según manual y política vigente? | MAN-REV dice aprobación desde 80; POL-DEC referencia 85 y condiciones. Explicitar conflicto. | MAN-REV@1#s01:01; POL-DEC@2#s02:01 |
| V01 | ¿Una señal de fraude activa resta 20 puntos o prevalece sobre el puntaje? | Vigente v2: no resta puntos; deriva a revisión cualquiera sea el puntaje. | POL-DEC@2#s04:01 |
| V02 | ¿Puede un diseñador de flujos cambiar umbrales con efecto inmediato? | Vigente v2 exige dos supervisores de la organización; una aprobación no entra en vigor. | POL-DEC@2#s05:01 |

**Decisión de Francisca Meyer:** aprueba las 20 preguntas y expectativas.
**Fecha:** 7 de noviembre de 2026. **Observaciones:** aprobación comunicada en este chat; registro separado en `evaluation/cierre_v3_20261107/aprobacion_cliente.json`. No se presenta como firma digital ni como revisión de respuestas generadas.

Si se solicitan cambios, crear otra versión y conservar este conjunto; no ajustar retroactivamente las preguntas para mejorar resultados.
