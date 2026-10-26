param([string]$Python312 = '')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
if (-not (Test-Path -LiteralPath '.venv\Scripts\python.exe')) {
    if ($Python312) { & $Python312 -m venv .venv }
    elseif (Get-Command py -ErrorAction SilentlyContinue) { py -3.12 -m venv .venv }
    else { python -m venv .venv }
    if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el entorno. Instala Python 3.12 o indica -Python312.' }
}
& '.\.venv\Scripts\python.exe' -m pip install -r requirements-lock.txt
if ($LASTEXITCODE -ne 0) { throw 'No se pudieron instalar las dependencias.' }
& '.\.venv\Scripts\python.exe' -m mira.cli preparar
if ($LASTEXITCODE -ne 0) { throw 'No se pudo preparar el proyecto.' }
