@echo off

set "CONDA_ROOT_PREFIX=%cd%\portable_env\conda"

REM Run the Python script silently with the desired process name
"%CONDA_ROOT_PREFIX%\python.exe" "windows_startup.py"
