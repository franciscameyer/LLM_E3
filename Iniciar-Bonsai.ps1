param(
    [string]$LlamaServer = 'C:\Users\PC RST\Desktop\Bonsai\llama-prism-b10743-adfffbe-bin-win-cuda-12.4-x64\llama-server.exe',
    [string]$Modelo = 'C:\Users\PC RST\Desktop\Bonsai\llama-prism-b10743-adfffbe-bin-win-cuda-12.4-x64\Bonsai-27B\Ternary-Bonsai-2-27B-PQ2_0.gguf',
    [string]$Cuda12 = 'C:\Users\PC RST\miniconda3\Lib\site-packages\torch\lib',
    [int]$Puerto = 8080
)
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $LlamaServer)) { throw 'No se encuentra llama-server.exe. Indica -LlamaServer.' }
if (-not (Test-Path -LiteralPath $Modelo)) { throw 'No se encuentra el GGUF. Indica -Modelo.' }
$taskPreviousPath = $env:PATH
try {
    if (Test-Path -LiteralPath (Join-Path $Cuda12 'cudart64_12.dll')) { $env:PATH = $Cuda12 + ';' + $env:PATH }
    & $LlamaServer --model $Modelo --alias bonsai-27b --host 127.0.0.1 --port $Puerto --ctx-size 8192 --parallel 1 --n-gpu-layers all --cache-type-k q4_0 --cache-type-v q4_0 --flash-attn on --batch-size 512 --ubatch-size 128 --jinja --reasoning off
    if ($LASTEXITCODE -ne 0) { throw "llama.cpp termino con codigo $LASTEXITCODE. Revisa las bibliotecas CUDA y la memoria disponible." }
} finally { $env:PATH = $taskPreviousPath }
