@echo off
REM Script de configuração para Windows 11 PowerShell
REM Este arquivo resolve problemas comuns de instalação

echo.
echo ====================================================
echo  Configurador Django - Windows 11
echo ====================================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não foi encontrado no PATH
    echo Por favor, instale Python 3.13+ de python.org
    pause
    exit /b 1
)

REM Verificar versão do Python
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Python detectado: %PYTHON_VERSION%
echo.

REM Criar ambiente virtual se não existir
if not exist "venv" (
    echo [CRIANDO] Ambiente virtual...
    python -m venv venv
    echo [OK] Ambiente virtual criado!
) else (
    echo [INFO] Ambiente virtual já existe
)

REM Ativar ambiente virtual
echo [ATIVANDO] Ambiente virtual...
call venv\Scripts\activate.bat

REM Executar script de instalação Python
echo.
echo [EXECUTANDO] Script de instalação...
python setup_windows.py

if errorlevel 1 (
    echo.
    echo [ERRO] Houve um problema na instalação
    pause
    exit /b 1
)

echo.
echo [SUCESSO] Tudo pronto!
echo.
pause
