@echo off
REM ==================== NZBGeek Submission Script Launcher ====================
REM Este arquivo executa o script Python submit_nzbs.py
REM =============================================================================

setlocal

REM Obtém o diretório do script
set "SCRIPT_DIR=%~dp0"
set "PYTHON_SCRIPT=%SCRIPT_DIR%submit_nzbs.py"

REM Verifica se o Python está instalado
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao encontrado!
    echo.
    echo Por favor, instale o Python 3.7 ou superior.
    echo Download: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Verifica se o script Python existe
if not exist "%PYTHON_SCRIPT%" (
    echo [ERRO] Script nao encontrado: %PYTHON_SCRIPT%
    echo.
    pause
    exit /b 1
)

REM Executa o script Python
python "%PYTHON_SCRIPT%"

REM Captura o código de saída
set EXIT_CODE=%errorlevel%

REM Se houver erro, mostra mensagem
if %EXIT_CODE% neq 0 (
    echo.
    echo [ERRO] O script terminou com erro (codigo: %EXIT_CODE%)
    echo.
    pause
)

endlocal
exit /b %EXIT_CODE%
