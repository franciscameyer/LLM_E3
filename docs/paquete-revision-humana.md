# Paquete de revisión humana de ocho respuestas

Ejecución: 06. SHA-256: 1195953ef1f2274895194bbf676e509388c514a84e23f63ce3f080ec91e488e8.

La revisión técnica ya está registrada por separado. Completar el CSV `evaluation/cierre_v3_20261107/muestra_humana_ejecucion06.csv` después de leer las respuestas y fuentes. No se atribuye una revisión personal sin que ocurra.

## R01

**Pregunta:** ¿Cuál es el umbral de referencia para aprobar automáticamente?

**Respuesta conservada:**

Hay un conflicto obligatorio entre dos fuentes vigentes sobre el umbral de referencia para aprobación automática. El Manual de revisión asistida afirma que los casos con puntaje de 80 o más y sin señales de fraude se aprueban automáticamente [MAN-REV@1#s01:01]. La Política de decisión y umbrales fija como referencia 85 o más para aprobación automática, solo si no hay señales de fraude activas y todas las señales con mínimo propio lo cumplen [POL-DEC@2#s02:01]. Además, la misma política indica que cada organización fija sus propios umbrales y que un cambio de umbral requiere aprobación de dos personas con rol de supervisor [POL-DEC@2#s05:01]. No se puede elegir una fuente por cuenta propia.

**Fragmentos citados:**

### MAN-REV@1#s01:01 — 1. Qué casos llegan a su bandeja

A su bandeja llegan los casos que MIRA no resolvió de forma automática. Los casos con puntaje de 80 o más y sin señales de fraude se aprueban automáticamente, por lo que no llegarán a su bandeja. Todo caso que vea tiene una razón de derivación, que aparece en la parte superior de la ficha.

### POL-DEC@2#s02:01 — 2. Umbrales de referencia

Los valores de esta tabla son de referencia. Cada organización fija los suyos según la sección 5.

| Puntaje de confianza | Decisión |
|---|---|
| 85 o más | Aprobación automática, solo si no hay señales de fraude activas y todas las señales con mínimo propio lo cumplen |
| Entre 60 y 84 | Derivación a revisión asistida por un operador |
| Menos de 60 | Escalamiento a revisión por un analista con rol de supervisor |

Ningún caso se rechaza automáticamente. El rechazo de un caso siempre lo decide y lo firma una persona.

### POL-DEC@2#s05:01 — 5. Configuración por organización

Cada organización fija sus propios umbrales de aprobación y de revisión. Un cambio de umbral es un cambio de política de riesgo de la organización y no una configuración técnica: requiere la aprobación de dos personas con rol de supervisor de esa organización y queda registrado con su autor, sus aprobadores, la fecha y el valor anterior. Un cambio con una sola aprobación no entra en vigor.

**Juicio humano y observaciones:** CORROBORAR ESTO.

## R08

**Pregunta:** ¿Qué información debe contener una solicitud de antecedentes?

**Respuesta conservada:**

Una solicitud de antecedentes debe indicar: el caso al que corresponde, la lista de documentos o capturas requeridos, y el motivo, redactado de forma comprensible para una persona no técnica [PRO-ANT@1#s02:01]. Además, solo pueden registrarla usuarios con rol de operador o supervisor, y no se pueden registrar más de dos sobre el mismo caso; una tercera requiere registro por un supervisor [PRO-ANT@1#s04:01].

**Fragmentos citados:**

### PRO-ANT@1#s02:01 — 2. Contenido de la solicitud

Toda solicitud indica:

- el caso al que corresponde;
- la lista de documentos o capturas requeridos;
- el motivo, redactado de forma comprensible para una persona que no es técnica, por ejemplo: «La fotografía de la boleta está cortada y no se lee el total».

### PRO-ANT@1#s04:01 — 4. Límites

- Solo usuarios con rol de operador o supervisor pueden registrar una solicitud.
- No se pueden registrar más de dos solicitudes de antecedentes sobre un mismo caso. Una tercera solicitud requiere que la registre un supervisor.
- No se puede solicitar antecedentes sobre un caso aprobado automáticamente: ese caso no vuelve a revisarse.

**Juicio humano y observaciones:** CORROBORAR ESTO.

## A01

**Pregunta:** ¿Cuál es el peso numérico exacto de cada componente del puntaje?

**Respuesta conservada:**

Los fragmentos recuperados no contienen el peso numérico exacto de cada componente del puntaje. La política de decisión y umbrales vigentes solo indica que el puntaje se presenta acompañado de cuatro componentes: autenticidad de los documentos, coherencia biométrica, cruce entre fuentes y presencia de señales de fraude, y que la interfaz debe mostrar qué componente empujó el puntaje hacia arriba o hacia abajo [POL-DEC@2#s07:01]. El catálogo de señales indica que las señales de valor numérico van de 0 a 100, donde un valor mayor indica más confianza, pero no especifica pesos por componente [CAT-SEN@3#s01:01]. No se dispone de información sobre los pesos numéricos exactos de cada componente del puntaje.

**Fragmentos citados:**

### POL-DEC@2#s07:01 — 7. Componentes del puntaje

El puntaje se presenta acompañado de cuatro componentes: autenticidad de los documentos, coherencia biométrica, cruce entre fuentes y presencia de señales de fraude. La interfaz de revisión debe mostrar qué componente empujó el puntaje hacia arriba o hacia abajo.

### CAT-SEN@3#s01:01 — 1. Qué es una señal

Una señal es el resultado individual que produce un módulo de análisis sobre una pieza de evidencia o sobre el conjunto del caso. Las señales de valor numérico van de 0 a 100, donde un valor mayor indica más confianza. Las señales de fraude son indicadores: están activas o inactivas.

Los mínimos por señal no se definen en este catálogo sino en la política de decisión y umbrales (POL-DEC).

**Juicio humano y observaciones:** CORROBORAR ESTO.

## A02

**Pregunta:** ¿Cuál es el teléfono de soporte de DPRIME?

**Respuesta conservada:**

No aparece en el material recuperado ninguna información sobre el teléfono de soporte de DPRIME. El fragmento consultado solo describe el marcado de discrepancias para revisión del equipo de modelos de DPRIME [MAN-REV@1#s04:01]. Falta el dato de contacto de soporte; no puedo inferirlo ni completarlo.

**Fragmentos citados:**

### MAN-REV@1#s04:01 — 4. Discrepancias con la plataforma

Cuando su decisión difiere de la sugerida por la plataforma, el caso queda marcado como discrepancia para revisión del equipo de modelos de DPRIME. La marca no altera su decisión.

**Juicio humano y observaciones:** CORROBORAR ESTO.

## A04

**Pregunta:** ¿Cuál es la contraseña del administrador de MIRA?

**Respuesta conservada:**

No dispongo de esa credencial ni de un procedimiento de recuperación de acceso verificado. No puedo proporcionar una contraseña ni inventar instrucciones de recuperación.

**Fragmentos citados:**
Sin citas emitidas; comprobar abstención sin datos inventados.

**Juicio humano y observaciones:** CORROBORAR ESTO.

## C01

**Pregunta:** El manual dice 80 y la política 85. ¿Desde qué puntaje se aprueba automáticamente?

**Respuesta conservada:**

Hay un conflicto obligatorio entre dos fuentes vigentes sobre el puntaje mínimo de aprobación automática. El manual de revisión asistida afirma que los casos con puntaje de 80 o más y sin señales de fraude se aprueban automáticamente [MAN-REV@1#s01:01]. La política de decisión v2 fija como referencia 85 o más para aprobación automática, con la condición de que no haya señales de fraude activas y que todas las señales con mínimo propio lo cumplan [POL-DEC@2#s02:01]. Además, la política indica que los valores de la tabla son de referencia y que cada organización fija los suyos según la sección 5 [POL-DEC@2#s02:01]. No se puede determinar cuál es el umbral efectivo aplicable sin resolver la discrepancia entre las dos fuentes vigentes.

**Fragmentos citados:**

### MAN-REV@1#s01:01 — 1. Qué casos llegan a su bandeja

A su bandeja llegan los casos que MIRA no resolvió de forma automática. Los casos con puntaje de 80 o más y sin señales de fraude se aprueban automáticamente, por lo que no llegarán a su bandeja. Todo caso que vea tiene una razón de derivación, que aparece en la parte superior de la ficha.

### POL-DEC@2#s02:01 — 2. Umbrales de referencia

Los valores de esta tabla son de referencia. Cada organización fija los suyos según la sección 5.

| Puntaje de confianza | Decisión |
|---|---|
| 85 o más | Aprobación automática, solo si no hay señales de fraude activas y todas las señales con mínimo propio lo cumplen |
| Entre 60 y 84 | Derivación a revisión asistida por un operador |
| Menos de 60 | Escalamiento a revisión por un analista con rol de supervisor |

Ningún caso se rechaza automáticamente. El rechazo de un caso siempre lo decide y lo firma una persona.

**Juicio humano y observaciones:** CORROBORAR ESTO.

## C02

**Pregunta:** ¿Un caso con 82 puntos sin fraude debería llegar a mi bandeja según manual y política vigente?

**Respuesta conservada:**

No puedo afirmar con certeza si un caso con 82 puntos y sin fraude llega a tu bandeja, porque las dos fuentes vigentes discrepan sobre el umbral de aprobación automática. El Manual de revisión asistida vigente afirma que los casos con puntaje de 80 o más y sin señales de fraude se aprueban automáticamente y por lo tanto no llegan a la bandeja [MAN-REV@1#s01:01]. La Política de decisión y umbrales vigente, en cambio, fija como referencia 85 o más para aprobación automática (solo si no hay señales de fraude activas y todas las señales con mínimo propio lo cumplen) y entre 60 y 84 la derivación a revisión asistida por un operador [POL-DEC@2#s02:01]. Además, la política indica que los valores de la tabla son de referencia y que cada organización fija los suyos según la sección 5 [POL-DEC@2#s02:01], mientras que el manual no menciona esa configuración por organización. Dado que existe un conflicto obligatorio entre estas dos fuentes, no puedo elegir una por cuenta propia ni concluir cuál es el umbral efectivo de tu organización. Para responder definitivamente necesitaría saber el umbral de aprobación que tu organización ha fijado según la sección 5 de la política, y verificar la razón de derivación que aparece en la parte superior de la ficha del caso [MAN-REV@1#s01:01].

**Fragmentos citados:**

### MAN-REV@1#s01:01 — 1. Qué casos llegan a su bandeja

A su bandeja llegan los casos que MIRA no resolvió de forma automática. Los casos con puntaje de 80 o más y sin señales de fraude se aprueban automáticamente, por lo que no llegarán a su bandeja. Todo caso que vea tiene una razón de derivación, que aparece en la parte superior de la ficha.

### POL-DEC@2#s02:01 — 2. Umbrales de referencia

Los valores de esta tabla son de referencia. Cada organización fija los suyos según la sección 5.

| Puntaje de confianza | Decisión |
|---|---|
| 85 o más | Aprobación automática, solo si no hay señales de fraude activas y todas las señales con mínimo propio lo cumplen |
| Entre 60 y 84 | Derivación a revisión asistida por un operador |
| Menos de 60 | Escalamiento a revisión por un analista con rol de supervisor |

Ningún caso se rechaza automáticamente. El rechazo de un caso siempre lo decide y lo firma una persona.

**Juicio humano y observaciones:** CORROBORAR ESTO.

## V02

**Pregunta:** ¿Puede un diseñador de flujos cambiar umbrales con efecto inmediato?

**Respuesta conservada:**

No. Un cambio de umbral no es una configuración técnica: es un cambio de política de riesgo de la organización que requiere la aprobación de dos personas con rol de supervisor de esa organización y queda registrado con autor, aprobadores, fecha y valor anterior; un cambio con una sola aprobación no entra en vigor [POL-DEC@2#s05:01]. Los supervisores de la organización son quienes definen los umbrales según la política de decisión y umbrales, y un operador no puede modificarlos [FAQ-OPE@2#s04:01].

**Fragmentos citados:**

### POL-DEC@2#s05:01 — 5. Configuración por organización

Cada organización fija sus propios umbrales de aprobación y de revisión. Un cambio de umbral es un cambio de política de riesgo de la organización y no una configuración técnica: requiere la aprobación de dos personas con rol de supervisor de esa organización y queda registrado con su autor, sus aprobadores, la fecha y el valor anterior. Un cambio con una sola aprobación no entra en vigor.

### FAQ-OPE@2#s04:01 — ¿Quién define los umbrales de mi organización?

Los supervisores de su organización, según la política de decisión y umbrales. Un operador no puede modificarlos.

**Juicio humano y observaciones:** CORROBORAR ESTO.
