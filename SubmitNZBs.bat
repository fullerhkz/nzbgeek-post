@echo off
setlocal

:: Configurações do script
set "POWERSHELL_EXE=powershell.exe"
set "TERMINAL_EXE=wt.exe"
set "SCRIPT_PATH=C:\Scripts\Submit NZBGeek\SubmitNZBs.ps1"
set "PROFILE_NAME=NZBGeek Profile"

:: Verificar se o Windows Terminal está instalado
where %TERMINAL_EXE% >nul 2>&1
if %errorlevel% equ 0 (
    echo Abrindo Windows Terminal com perfil "%PROFILE_NAME%"...
    start "" %TERMINAL_EXE% -p "%PROFILE_NAME%" %POWERSHELL_EXE% -Command "& '%SCRIPT_PATH%'"
) else (
    echo Abrindo PowerShell com configuração personalizada...
    start "" %POWERSHELL_EXE% -WindowStyle Maximized -ExecutionPolicy Bypass -Command "& { $Host.UI.RawUI.BackgroundColor = 'DarkBlue'; $Host.UI.RawUI.ForegroundColor = 'White'; Clear-Host; & '%SCRIPT_PATH%' }"
)

endlocal