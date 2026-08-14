@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Criando ambiente virtual...
    python -m venv .venv
)

echo [INFO] Instalando dependencias...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo [INFO] Ambiente pronto.
pause