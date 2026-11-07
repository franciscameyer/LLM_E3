# Corpus y discrepancias del CU-1

El corpus contiene seis fuentes ficticias del kit docente y un extracto de la
Descripción del proyecto MIRA v1.4. El inventario
automático conserva archivo, código, título, versión, estado, vigencia, huella
SHA-256 y tamaño aproximado en tokens (palabras / 0,75; no es el tokenizador de Bonsai).

| Código | Versión | Estado declarado | Inicio de vigencia |
| --- | --- | --- | --- |
| POL-DEC | 1 | Derogada | 2026-03-02; termina 2026-08-31 |
| POL-DEC | 2 | Vigente | 2026-09-01 |
| CAT-SEN | 3 | Vigente | 2026-09-01 |
| FAQ-OPE | 2 | Vigente | 2026-10-01 |
| MAN-REV | 1 | Vigente | 2026-07-15 |
| PRO-ANT | 1 | Vigente | 2026-07-15 |
| MIRA-DESC | 1.4 | Contexto de levantamiento | Documento del 2026-08-12, sin vigencia normativa declarada |

## Conflicto documental vigente

MAN-REV v1 §1 afirma aprobación automática desde 80 y sin señales de fraude.
POL-DEC v2 §2 establece 85 como referencia, condicionado a mínimos por señal,
ausencia de fraude y configuración por organización (§5). Ambos se declaran
vigentes. La aplicación recupera ambos cuando la consulta trata esa discrepancia;
no declara que el manual esté derogado ni decide una precedencia que el kit no fija.

## Cambios entre versiones

POL-DEC v1 §4 descontaba 20 puntos por fraude; v2 §4 dispone derivación a revisión
cualquiera sea el puntaje, sin restar puntos. V1 §3 permitía cambiar umbrales a un
diseñador con efecto inmediato; v2 §5 exige aprobación de dos supervisores.
V1 §5 calculaba con señales disponibles; v2 §6 impide aprobación con una señal faltante.

## Discrepancia entre base y política

El Excel reporta umbral de aprobación 90 para ORG-01 y C-012 está derivado con 86.
El cambio CU-001 de 85 a 90 identifica solo un aprobador. POL-DEC v2 §5 dice que una
sola aprobación no entra en vigor. Se conserva el motivo que reporta la plataforma
y se muestra la discrepancia. El asistente no corrige la base ni da por acreditada
la validez normativa del cambio.

## Manipulación y evidencia insuficiente

La evidencia E-007 de C-014 incluye una instrucción dirigida al asistente que pide
ignorar políticas y aprobar. No es autorización de la persona ni una regla del corpus.
Se conserva el original y se aísla esa instrucción en el resultado mostrado al modelo.

C-018 carece de CRUCE_MONTO. La ausencia de esa señal no implica que cumpla el mínimo.
C-016 ya tiene dos solicitudes: U-01 no puede registrar la tercera; un supervisor
sí puede, después de confirmar. C-020 incluye un documento en portugués; no se
inventa una política general de idiomas a partir de ese dato.

## Descripción MIRA v1.4

Los extractos en `corpus/descripcion/MIRA_v1.4.md` reproducen §§2.6, 2.7, 2.11 y
2.13. El inventario registra el origen `Descripción`, el documento original,
su fecha y SHA-256. La recuperación de contexto se activa al pedir explícitamente
la Descripción, el levantamiento o v1.4. Las políticas del kit mantienen sus IDs
y su filtro de vigencia.

- **Decisión.** §2.6 menciona aprobación sobre 85 y también a partir de 80. MAN-REV
  v1 §1 usa 80 y POL-DEC v2 §2 usa 85 como referencia configurable y condicionada.
  La Descripción admite escalar o rechazar bajo 60. POL-DEC v2 §2 indica escalamiento
  y reserva el rechazo a una persona. Se exige citar las tres fuentes al contrastar.
- **Configuración.** §§2.6 y 2.13 atribuyen la configuración al diseñador. POL-DEC
  v2 §5 exige dos supervisores para aprobar el cambio. Se muestran ambos textos
  y se distingue el procedimiento del dato configurado de una organización.
- **Revisión y auditoría.** §§2.7 y 2.11 describen necesidades del producto, como
  descargar el rastro y conservar evidencia durante 90 días. Las respuestas
  atribuyen esas afirmaciones al levantamiento. El alcance implementado se verifica
  mediante la especificación de CU-1 y las trazas de MCP.

El capítulo 7 de entrevistas queda como antecedente para el equipo. Los artefactos
y la retroalimentación de las entregas 1 y 2 quedan por contrastar.

La pauta también menciona D1–D8 y v3.0 sin definirlos en las páginas adjuntas;
el guion de demostración propuesto no se presenta como una transcripción de esos pasos.
