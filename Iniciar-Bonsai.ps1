param(
    [string]$LlamaServer = '',
    [string]$Modelo = '',
    [string]$Cuda12 = '',
    [int]$Puerto = 8080
)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) { throw 'Falta .venv. Ejecuta Instalar-MIRA.ps1.' }
$taskModelArgs = @('-m', 'mira.launch_model', '--port', "$Puerto")
if ($LlamaServer) { $taskModelArgs += @('--server', $LlamaServer) }
if ($Modelo) { $taskModelArgs += @('--model', $Modelo) }
if ($Cuda12) { $taskModelArgs += @('--cuda12', $Cuda12) }
# Un solo lanzador mantiene la misma configuración para CMD, PowerShell y .env.
& '.\.venv\Scripts\python.exe' @taskModelArgs
if ($LASTEXITCODE -ne 0) { throw "llama.cpp termino con codigo $LASTEXITCODE. Revisa las rutas en .env, CUDA y la memoria disponible." }
