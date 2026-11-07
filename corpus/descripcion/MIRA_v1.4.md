# Descripción del proyecto MIRA · extractos para CU-1

| Campo | Valor |
|---|---|
| Código | MIRA-DESC |
| Versión | 1.4 |
| Estado | Contexto |
| Vigencia | No declarada como norma |
| Fecha del documento | 12 de agosto de 2026 |
| Fuente original | MIRA-descripcion-proyecto .docx |
| SHA-256 original | 904c977f1be7215352805e9d19cd96affbaa5c6fd1499aff09438b80b623d9de |

Extractos de la descripción docente elaborada por la Dirección de Producto de DPRIME. Se conservan los títulos y párrafos originales de las cuatro secciones seleccionadas.

## 2.6 El nivel de confianza y la decisión

Cada caso analizado recibe un puntaje de confianza entre 0 y 100, que resume las señales obtenidas. El puntaje se acompaña de sus componentes, para que quien lo lea entienda qué lo empujó hacia arriba o hacia abajo: autenticidad de los documentos, coherencia biométrica, cruce entre fuentes y presencia de señales de fraude.

Ese puntaje se traduce en una decisión mediante umbrales configurables. Los valores de referencia son: sobre 85, el caso se aprueba automáticamente sin intervención humana; entre 60 y 84, se deriva a revisión asistida por un operador; bajo 60, se escala o se rechaza por riesgo alto. Estos rangos deben poder ajustarse por cliente y por tipo de proceso desde el propio diseñador de flujos, sin intervención de DPRIME.

La aprobación automática debe aplicarse a partir de 80 puntos cuando el caso no presente ninguna señal de fraude activa.

Cuando el puntaje sea suficiente pero alguna señal individual esté por debajo de su mínimo, el caso debe derivarse a revisión aunque el total lo permita. El detalle de qué señales tienen mínimo propio y cuáles son sus valores está pendiente de definir con el área de riesgo del cliente piloto.

## 2.7 La revisión asistida

Los casos que no se resuelven solos llegan a una bandeja de trabajo. Esta parte del producto casi no existe hoy y es, según el cliente piloto, la que decide si la plataforma se usa o no.

El operador debe ver, en una sola pantalla, la evidencia del caso, el puntaje obtenido, el desglose de las señales y —sobre todo— la razón por la cual el caso fue derivado. Debe poder abrir cada pieza de evidencia, ver qué encontró la plataforma en ella y en qué parte del documento o de la imagen lo encontró.

El operador resuelve el caso: aprueba, rechaza o solicita antecedentes adicionales. Su decisión y el motivo quedan registrados. Cuando la decisión del operador difiere de lo que la plataforma sugería, esa discrepancia debe quedar marcada de manera que el equipo de modelos pueda revisarla después.

Un caso derivado a revisión debe resolverse dentro del plazo comprometido por el cliente con sus propios asegurados, de modo que la plataforma debe mostrar el tiempo restante y alertar cuando un caso lleve demasiado tiempo detenido.

## 2.11 Trazabilidad y auditoría

Todo lo que la plataforma hace sobre un caso debe quedar registrado: qué evidencia entró, qué módulos se ejecutaron, en qué versión, qué devolvió cada uno, qué reglas se aplicaron, qué puntaje resultó, qué decisión se tomó y quién intervino. Ese rastro debe poder consultarse desde la interfaz y descargarse.

El rastro es inalterable. Ningún usuario, incluido el administrador de la cuenta del cliente y el personal de DPRIME, puede modificarlo ni eliminarlo.

Debe ser posible reconstruir una decisión pasada tal como se tomó, es decir, con las versiones de los módulos y del flujo que estaban vigentes en ese momento. Una decisión que no se puede reproducir no se puede defender.

La evidencia y los resultados se conservan noventa días, plazo tras el cual la evidencia original se elimina y se conserva únicamente el registro de la decisión.

## 2.13 Cuentas, perfiles y aislamiento

Cada cliente es una organización independiente dentro de la plataforma, con sus propios usuarios, flujos, módulos activos, umbrales y datos. Bajo ninguna circunstancia un cliente puede ver información de otro, y esa separación debe poder demostrarse ante una auditoría, no solo afirmarse.

Dentro de una organización, los permisos deben distinguir al menos entre quien opera casos, quien diseña flujos, quien consulta indicadores y quien administra la cuenta. La configuración de los umbrales de decisión corresponde a quien diseña flujos.

Los usuarios de los clientes se autentican con las credenciales que administra la propia plataforma. Los clientes de mayor tamaño exigen federar la autenticación contra su propio directorio corporativo.
