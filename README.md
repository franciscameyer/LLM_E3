# MIRA · CU-1: asistente del operador de revisión

Aplicación local para explicar derivaciones con evidencia documental y consultar
datos del kit mediante un servidor MCP propio. El modelo de generación es tu
**Bonsai 27B, servido por llama.cpp**. La interfaz y los mensajes están en español.

## Abrir en este equipo

El entorno `.venv` ya está instalado y el kit está importado e indexado.

1. Abre `Iniciar-Bonsai.cmd` con doble clic o ejecútalo en la terminal:

   ```powershell
   .\Iniciar-Bonsai.cmd
   ```

   Espera el mensaje `listening on http://127.0.0.1:8080`.

2. Abre `Iniciar-MIRA.cmd` con doble clic, o ejecuta:

   ```powershell
   .\Iniciar-MIRA.cmd
   ```

3. Visita **http://127.0.0.1:8000**. Usuario inicial: **U-01**, contraseña de
   demostración: **mira-demo**. El selector permite probar los otros roles del kit.

Los dos procesos permanecen en sus terminales; `Ctrl+C` los detiene. Los scripts
no cambian la política de ejecución de PowerShell. Si bloquea un `.ps1`, utiliza
los comandos equivalentes descritos abajo o la política autorizada de tu equipo.

Esta es una demostración local con datos ficticios y contraseña compartida.
La separación por rol y organización se valida en el servidor; el acceso de
demostración no reemplaza una autenticación de producción.

## Qué probar

| Escenario | Acción |
| --- | --- |
| Datos y norma | Selecciona C-012 y pregunta por qué se derivó con 86 puntos. Abre las citas y las trazas. |
| Conflicto vigente | Pregunta por la diferencia entre 80 del manual y 85 de la política. Debe presentar ambas fuentes. |
| Dato ausente | Pregunta por los pesos exactos de los componentes. No están en el corpus. |
| Vigencia | Pregunta si una señal de fraude resta 20 puntos. La regla vigente v2 dice que prevalece. |
| Manipulación | Revisa C-014. La instrucción ajena de E-007 se aísla y no autoriza aprobar. |
| Límite | Como U-01, intenta preparar una solicitud para C-016. Ya tiene dos; debe bloquearse. |
| Rol | Cambia a U-03: puede consultar documentos, pero no fichas individuales. |
| Organización | Como U-01, pregunta por C-020. El servidor deniega el acceso. Como U-04 sí pertenece a su organización. |
| Confirmación | Prepara antecedentes para C-011: primero aparece una propuesta. Solo el botón confirmado registra la solicitud. |

El caso C-012 trae además una discrepancia de datos: el umbral reportado de ORG-01
es 90, pero CU-001 tiene solo una aprobación. La aplicación conserva ambos hechos
y advierte que el historial no acredita el requisito de POL-DEC §5 v2.

`Solo documentos` consulta el RAG por MCP y muestra fragmentos; no pretende ser
una respuesta generada. Sirve para revisar recuperación cuando el modelo está apagado.
Si el modelo falla, el chat muestra el error y no sustituye su respuesta con una invención.

El modelo usa referencias cortas asignadas al contexto; la interfaz recibe las citas
originales con fuente/sección/versión. La ficha incorpora reglas recuperadas desde
el motivo de derivación y el contexto prioriza las fuentes nuevas. Las peticiones
directas de credenciales reciben abstención sin inventar recuperación de acceso.

## Configuración del modelo

La configuración predeterminada usa `http://127.0.0.1:8080/v1`, descubre el nombre
desde `/v1/models` y llama `/v1/chat/completions`. No envía datos a un proveedor externo.
Copia `.env.example` como `.env` para cambiar URL, modelo, timeout o límite de salida.
Nunca versiones claves ni `.env`.

`mira/launch_model.py` contiene las rutas verificadas del ejecutable y del GGUF en
este equipo. Acepta `--server`, `--model`, `--cuda12` y `--port` para otro entorno.
También lee `LLAMA_SERVER`, `LLAMA_MODEL` y `LLAMA_CUDA12` de `.env`.
El lanzador PowerShell delega en ese mismo módulo y acepta parámetros equivalentes.
El ejecutable necesita CUDA 12: el script añade al PATH de su proceso las DLL ya
instaladas en `miniconda3/Lib/site-packages/torch/lib`. La carpeta de llama.cpp
contenía DLL de CUDA 13, insuficientes para esos binarios. El PATH global no cambia.

Para la GPU de 8 GB se usa contexto de 8192 tokens, una sola conversación en
inferencia, caché K/V q4_0 y lotes reducidos. El modelo puede ser lento; evita
lanzar varias conversaciones o la evaluación completa mientras haces una demo.
El contexto de un solo intercambio se conserva durante el bucle de herramientas;
no se envía al modelo el historial de conversaciones anteriores.

El modo `LLM_TOOL_MODE=native` usa llamadas de función de llama.cpp. Si otra
plantilla no las admite, `LLM_TOOL_MODE=json` habilita un adaptador explícito:
el modelo propone nombre y argumentos JSON y el mismo cliente MCP los valida
y ejecuta. La interfaz de negocio y la confirmación no cambian.

## Comandos sin activar el entorno

```powershell
# Preparación repetible: verifica originales y reconstruye solo el índice documental
.\.venv\Scripts\python.exe -m mira.cli preparar

# Estado del modelo
.\.venv\Scripts\python.exe -m mira.cli estado

# Recuperación, sin generación
.\.venv\Scripts\python.exe -m mira.cli buscar "¿Qué indica FRA_MEMORIA?"

# Conversación con modelo y MCP reales
.\.venv\Scripts\python.exe -m mira.cli preguntar "¿Por qué se derivó C-012?" --usuario U-01

# Pruebas aisladas (no modifican la base de la demo)
.\.venv\Scripts\python.exe -m pytest -q

# Comparación de recuperación
.\.venv\Scripts\python.exe -m mira.cli evaluar

# Evaluación de las 20 preguntas, con Bonsai encendido; puede tardar bastante
.\.venv\Scripts\python.exe -m mira.cli evaluar --generacion

# Conservar otra ejecución sin sobrescribir las anteriores
.\.venv\Scripts\python.exe -m mira.cli evaluar --generacion --salida evaluation/ejecucion_nueva

# Comparar fragmentaciones que realmente producen contenidos distintos
.\.venv\Scripts\python.exe -m mira.validation comparar --salida .cache/comparacion-nueva.json

# Cliente MCP externo y preguntas exploratorias en una base temporal aislada
.\.venv\Scripts\python.exe -m mira.check_delivery --generacion --salida .cache/verificacion-nueva.json
```

Usa siempre el Python de `.venv`, para no ejecutar el proyecto desde el entorno
`base` de Conda sin las dependencias. En VS Code está preconfigurado ese intérprete.

## MCP externo

`.vscode/mcp.json` incluye un cliente de demostración vinculado a U-01. El comando
equivalente para otro cliente es:

```powershell
.\.venv\Scripts\python.exe -m mira.cli mcp --usuario U-01 --sesion cliente-externo
```

El cliente debe iniciarlo por STDIO desde la raíz del proyecto. Este modo es para
desarrollo local: la selección de usuario en el lanzamiento no es autenticación
remota. El servidor publica herramientas, un recurso de inventario y un prompt.
La herramienta de confirmación exige una autorización firmada que el modelo no
recibe; las acciones se confirman en la aplicación web.

## Datos y reglas

Los seis Markdown y las siete tablas de CU-1 se leen del kit sin editarlo. SQLite
conserva los registros importados; las solicitudes nuevas se añaden y el estado
actual de un caso se representa mediante eventos. Los originales permanecen
disponibles y la preparación verifica sus valores contra el Excel.

La solicitud y el evento se registran en una transacción con revalidación de
límites, organización, rol, estado, sesión y caducidad. Repetir la misma
confirmación no duplica el efecto. El aviso al sistema de origen se guarda en
una **cola simulada**: el kit no proporciona un callback real.

El RAG usa BM25 local, con secciones de Markdown, metadatos de versión y vigencia
e IDs estables de fragmento. Es recuperación léxica real; no usa embeddings ni
una base vectorial. Chroma es opcional en la pauta. Esta elección evita cargar
otro modelo en el equipo; sus límites de sinónimos se evalúan en el golden set.
El registro del conflicto MAN-REV/POL-DEC es explícito y no elige una fuente.

El índice también incluye los extractos de la Descripción MIRA v1.4 (§2.6, §2.7,
§2.11 y §2.13) en `corpus/descripcion/MIRA_v1.4.md`. Preguntar por la Descripción
o por MIRA v1.4 activa su recuperación como contexto de levantamiento. En las
consultas operativas se buscan las políticas vigentes del kit. Los contrastes de
umbrales y permisos conservan las citas de cada fuente.

## Documentación y evaluación

- `docs/constitucion.md`: principios PR-1 a PR-7.
- `docs/arquitectura.md`: componentes, secuencia y contratos.
- `docs/analisis-corpus.md`: fuentes, discrepancias y límites del kit.
- `docs/estado-entrega.md`: cobertura y trabajo pendiente para la entrega académica.
- `docs/especificacion-cu1.md`: flujos, necesidades y requisitos con fuente y aceptación técnica.
- `docs/contratos-mcp.md`: entradas, salidas, permisos, efectos y errores.
- `docs/riesgos-controles.md`: controles, pruebas, límites y aporte del agente.
- `docs/reproduccion.md`: instalación, comparación experimental y ensayo técnico.
- `docs/validaciones-pendientes.md`: pendientes separados del cliente, docente y equipo.
- `evaluation/golden.json`: 20 preguntas fijadas antes del pipeline, commit `089b2fb`.
- `evaluation/resultados_recuperacion.json`: medición reproducible por fragmento.
- `evaluation/ejecucion_01/` y `evaluation/ejecucion_02/`: primera evaluación,
  fallo encontrado y resultados posteriores a la corrección. La segunda incluye
  `resumen.json`, huellas del código, respuestas y trazas.
- `evaluation/revision_manual.csv`: se genera al evaluar respuestas para registrar
  precisión de citas, fidelidad y revisión de conflicto/vigencia.
- `evaluation/cierre_tecnico/`: comparación por contenido completo, revisión
  semántica automatizada de la ejecución 02, muestra humana aún vacía, contratos
  obtenidos desde MCP real y comprobaciones de instalación/pruebas.
- `evaluation/ejecucion_03/`: nueva ejecución del golden con instrucciones de
  citas reforzadas y denegación determinista de acceso. Conserva respuestas,
  trazas, modelo efectivo y huellas; no reemplaza los históricos. Su revisión
  semántica automatizada registra dos fallos de fidelidad en C01/C02 y deja
  preparada una muestra para revisión humana independiente.
- `evaluation/ejecucion_04/`: ejecución de la versión con un solo reintento de citas
  inválidas, sin herramientas adicionales y sin debilitar el control de referencias.
  Completó las 20 preguntas sin errores estructurales; la revisión del agente marca
  19/20 fieles y deja la muestra humana vacía para validación independiente.
- `evaluation/ejecucion_05/`: evaluación tras corregir P07 y A04; las referencias
  cortas se resuelven a IDs originales, y las credenciales no se delegan al modelo.
  Incluye `muestra_revision_codex.csv` con ocho preguntas revisadas y
  `concordancia_interna_codex.json`; la revisión humana independiente sigue pendiente.
- `evaluation/correccion_citas_fidelidad/`: pruebas, repeticiones dirigidas y lectura
  del agente que conserva también los intentos previos fallidos y la sobrecitación residual.
- `evaluation/descripcion_v14/`: pruebas, contrastes con la Descripción y comparación
  de fragmentación. `evaluation/ejecucion_06/` conserva la reevaluación del golden.

Las respuestas esperadas siguen **pendientes de validación por el representante
del cliente**. La revisión semántica del agente se declara como automatizada:
falta una muestra humana independiente y su concordancia. Los resultados no
son métricas aprobadas por el cliente. D1–D8 y la etiqueta v3.0 requieren
aclaración del docente; el guion técnico es una propuesta del proyecto.

## Instalar en otro equipo

Instala Python 3.12 y ejecuta `Instalar-MIRA.ps1`. También puedes crear `.venv` con
`py -3.12 -m venv .venv`, instalar `requirements-lock.txt` y ejecutar `preparar`.
El entorno actual se creó con el Python 3.12 del runtime de Codex; si cambia esa
instalación, recrea el entorno con tu instalación estable de Python 3.12.

No copies `.data/session.key` ni la base activa como si fueran fuentes del kit.
Para una demo nueva, utiliza otra carpeta de datos con `MIRA_DATA_DIR`; la carga
creará una nueva base a partir del Excel sin borrar la ejecución anterior.

## Fuentes técnicas

- [Bonsai: ficha del modelo y servidor llama.cpp](https://huggingface.co/prism-ml/Ternary-Bonsai-27B-gguf)
- [llama.cpp: servidor y llamadas a herramientas](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)
- [FastMCP: cliente por STDIO](https://gofastmcp.com/clients/transports)
