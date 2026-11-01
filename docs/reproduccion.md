# Instalación, verificación y ensayo técnico

Plataforma probada: Windows x64, Python 3.12. El lock incluye pywin32; no se promete
instalación de ese lock sin cambios en Linux/macOS. No hace falta un modelo para
importar datos, comparar recuperación o ejecutar las pruebas con proveedor simulado.

## Instalación limpia

Desde una terminal PowerShell en la carpeta clonada:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m mira.cli preparar
.\.venv\Scripts\python.exe -m pytest -q
```

Se espera importar 3 organizaciones, 8 usuarios, 14 casos, 68 señales, 15 evidencias,
2 solicitudes originales y 2 cambios de umbral; índice de 6 documentos y 35 fragmentos.
Repetir `preparar` verifica originales y regenera el índice, sin resetear solicitudes.

## Configuración local del modelo

Copiar `.env.example` a `.env` y configurar rutas de la instalación propia:

```dotenv
LLAMA_SERVER=C:/ruta/llama-server.exe
LLAMA_MODEL=C:/ruta/Ternary-Bonsai-2-27B-PQ2_0.gguf
LLAMA_CUDA12=C:/ruta/bibliotecas-cuda12
LLM_BASE_URL=http://127.0.0.1:8080/v1
LLM_MODEL=auto
```

Las rutas deben existir y ser compatibles con los binarios. Los lanzadores CMD y
PowerShell delegan en `mira.launch_model`; también acepta `--server`, `--model`,
`--cuda12` y `--port`. `LLAMA_CUDA12` solo modifica PATH del proceso lanzado.
Los pesos y binarios se obtienen por separado; no están dentro del repositorio.
El nombre reportado por `/v1/models` es un alias, no un hash de los pesos.

```powershell
.\.venv\Scripts\python.exe -m mira.launch_model
# En otra terminal:
.\.venv\Scripts\python.exe -m mira.cli estado
.\.venv\Scripts\python.exe -m mira.cli servir
```

Abrir `http://127.0.0.1:8000`, usuario U-01, contraseña ficticia `mira-demo`.
Para una demo que admita repetir acciones sin alterar una ejecución anterior,
fijar `MIRA_DATA_DIR` a una carpeta NUEVA antes de preparar y servir:

```powershell
$env:MIRA_DATA_DIR = Join-Path $PWD '.cache/demo-nueva'
.\.venv\Scripts\python.exe -m mira.cli preparar
.\.venv\Scripts\python.exe -m mira.cli servir
```

No distribuir `.data`, `.env`, claves de sesión, entorno virtual ni base activa.
No borrar una base previa para simular que nunca se ejecutaron acciones.

## Evidencia reproducible sin sobrescribir históricos

```powershell
.\.venv\Scripts\python.exe -m mira.validation comparar --salida .cache/comparacion-nueva.json
.\.venv\Scripts\python.exe -m mira.cli evaluar --generacion --salida evaluation/ejecucion_nueva
.\.venv\Scripts\python.exe -m mira.check_delivery --generacion --salida .cache/verificacion-nueva.json
.\.venv\Scripts\python.exe -m mira.validation revision --ejecucion evaluation/ejecucion_02/resultados_generacion.json --juicios evaluation/cierre_tecnico/revision_semantica_agente.json --salida .cache/metricas-recalculadas.json
```

Los comandos con salida explícita rechazan reutilizar archivos de evidencia.
`check_delivery` prepara su propia base temporal, conecta un cliente MCP externo,
enumera tools/resources/prompts, comprueba denegaciones y prepara/cancela una
propuesta sin registrar solicitud. Con `--generacion` ejecuta ocho consultas nuevas
si el modelo está disponible. Conservar y revisar sus respuestas; no son preguntas
del golden ni tienen aprobación del cliente. Las pruebas pytest comprueban además
confirmación real, transacciones y concurrencia en bases aisladas.

La generación permite un solo reintento cuando hay IDs de cita desconocidos,
con el mismo contexto y sin nuevas herramientas. Se registra `reintento_citas`
en la salida; la segunda respuesta vuelve a pasar por todos los controles.
Si sigue citando IDs desconocidos, se retiene. Esto puede aumentar la latencia;
no garantiza fidelidad semántica ni funcionamiento de todas las paráfrasis.

Para repetir específicamente los dos fallos corregidos (P07: señal ausente en
C-018; A04: contraseña y recuperación no documentada), con Bonsai encendido:

```powershell
.\.venv\Scripts\python.exe -m mira.regression_check --salida .cache/regresion-nueva --repeticiones 3
```

Cada repetición usa una sesión distinta en una base temporal; guarda las salidas,
trazas y huellas después de cada pregunta. La comprobación estructural de P07
exige respuesta con POL-DEC v2 §6; A04 exige la abstención controlada sin citas.
Debe revisarse también el contenido; estas repeticiones dirigidas no son validación
humana ni una muestra independiente de consultas nuevas.

## Decisión de fragmentación

La comparación conserva el texto completo de cada objetivo del golden, aun cuando
se divide en varios fragmentos. No basta recuperar el nuevo fragmento `:01`.
Con k=6 se obtuvieron:

| Límite | Fragmentos del corpus | Objetivos completos | Preguntas con todos sus objetivos | Contexto base medio (caracteres) |
| --- | --- | --- | --- | --- |
| 300 | 50 | 10/18 | 8/16 | 1117,60 |
| 600 | 36 | 17/18 | 15/16 | 1678,10 |
| 900 | 35 | 18/18 | 16/16 | 1728,85 |
| 1800 | 35 | 18/18 | 16/16 | 1728,85 |

Se mantiene 1800: preserva secciones y tablas completas sin cambiar los IDs y
reglas de conflicto existentes. Empata con 900; no se afirma que sea superior.
300 reduce contexto pero pierde contenido; 600 pierde un objetivo. Esto mide
recuperación conservadora de secciones completas, no fidelidad ni latencia de LLM.
El ranking es BM25 más la relación explícita de conflicto del kit; complementos
fuera de k se excluyen del cómputo. No se atribuyen estas cifras a BM25 puro.

## Ensayo propuesto, sujeto a confirmación D1–D8

1. U-01: consultar C-012, abrir ficha y una cita con sección/versión; explicar 86,
   umbral reportado 90 y aprobación incompleta del cambio, sin darlo por vigente.
2. Preguntar pesos numéricos; mostrar abstención y qué información falta.
3. Preguntar manual 80 frente a política 85; abrir ambas fuentes vigentes.
4. Mostrar traza MCP de consulta, argumentos y resultado; no confundirlo con texto generado.
5. C-011: preparar, comprobar que aún no existe solicitud, confirmar expresamente,
   mostrar ID, cambio por evento y traza; no presentar el aviso simulado como callback real.
6. C-016 con U-01: mostrar rechazo del límite. C-014: mostrar instrucción aislada.
   U-03 y otra organización: mostrar denegación sin datos del caso.
7. Desde el cliente externo elegido, conectar STDIO con el comando del README,
   enumerar herramientas/recurso/prompt y ejecutar una consulta autorizada.
8. Otra persona formula una pregunta no ensayada; comprobar respuesta, abstención
   o error honesto y poder justificarlo con fuentes y trazas.

Todos los integrantes deben poder explicar el reparto RAG/MCP, el fallo R10 original,
la denegación corregida, los límites del muestreo y la diferencia entre cita válida
y respaldo semántico. Este listado no se atribuye al docente como guion oficial.
