@echo off
cd %~dp0

set "INSTALL_DIR=%cd%\portable_env"
set "CONDA_ROOT_PREFIX=%cd%\portable_env\conda"
set "MINICONDA_DOWNLOAD_URL=https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Windows-x86_64.exe"

echo Checking configuration.
if exist "%CONDA_ROOT_PREFIX%\python.exe" (
	
    set "conda_exists=T"
    echo conda portable already installed
) else (
    set "conda_exists=F"
    echo conda portable not installed
)

if "%conda_exists%"=="F" (

    echo Downloading and installing Miniconda.
    echo Downloading Miniconda from %MINICONDA_DOWNLOAD_URL% to %INSTALL_DIR%\miniconda_installer.exe
    mkdir "%INSTALL_DIR%"
    powershell -Command "Invoke-WebRequest %MINICONDA_DOWNLOAD_URL% -OutFile %INSTALL_DIR%\miniconda_installer.exe"
    start /wait "" "%INSTALL_DIR%\miniconda_installer.exe" /InstallationType=JustMe /NoRegistry=1 /AddToPath=0 /RegisterPython=0 /S /D=%CONDA_ROOT_PREFIX%
    echo Miniconda version:
    "%CONDA_ROOT_PREFIX%\Scripts\conda.exe" --version
)

set "PYTHONNOUSERSITE=1"
set "PYTHONPATH="
set "PYTHONHOME="
set "CUDA_PATH=%CONDA_ROOT_PREFIX%"
set "CUDA_HOME=%CUDA_PATH%"

call "%CONDA_ROOT_PREFIX%\Scripts\activate.bat" %CONDA_ROOT_PREFIX%

echo Configuring Miniconda
"%CONDA_ROOT_PREFIX%\Scripts\pip.exe" install -r requirements.txt --no-warn-script-location
"%CONDA_ROOT_PREFIX%\Scripts\pip.exe" install -r custom_requirements.txt --no-warn-script-location
"%CONDA_ROOT_PREFIX%\python.exe" update_data.py
