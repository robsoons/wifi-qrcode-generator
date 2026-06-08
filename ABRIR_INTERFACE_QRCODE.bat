@echo off
setlocal

cd /d "%~dp0"

set "PYTHON_EXE=c:\DEVMASTER\COTPYT\.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
  set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" "%~dp0interface_qrcode_wifi.py"
if errorlevel 1 (
  echo.
  echo Falha ao abrir a interface.
  echo Verifique se o Python e as dependencias estao instalados.
  pause
)

endlocal
