@echo off
cd %~dp0

set "CONDA_ROOT_PREFIX=%cd%\portable_env\conda"

set "PYTHONNOUSERSITE=1"
set "PYTHONPATH="
set "PYTHONHOME="
set "CUDA_PATH=%CONDA_ROOT_PREFIX%"
set "CUDA_HOME=%CUDA_PATH%"

call "%CONDA_ROOT_PREFIX%\Scripts\activate.bat" %CONDA_ROOT_PREFIX%

"%CONDA_ROOT_PREFIX%\python.exe" mykros_framework.py
