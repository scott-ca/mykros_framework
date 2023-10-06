#!/bin/bash

cd "$(dirname "${BASH_SOURCE[0]}")"

if [[ "$(pwd)" =~ " " ]]; then echo This script relies on Miniconda which can not be silently installed under a path with spaces. && exit; fi

OS_ARCH=$(uname -m)
case "${OS_ARCH}" in
    x86_64*)    OS_ARCH="x86_64";;
    arm64*)     OS_ARCH="aarch64";;
    aarch64*)     OS_ARCH="aarch64";;
    *)          echo "Unknown system architecture: $OS_ARCH! This script runs only on x86_64 or arm64" && exit
esac

# Config
INSTALL_DIR="$(pwd)/portable_env"
CONDA_ROOT_PREFIX="$(pwd)/portable_env/conda"
MINICONDA_DOWNLOAD_URL="https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-${OS_ARCH}.sh"

conda_exists="F"

# Checking if Miniconda needs needs to be installed
echo Checking configuration.
if "$CONDA_ROOT_PREFIX/bin/conda" --version &>/dev/null; then conda_exists="T"; fi

# (if necessary) install git and conda into a contained environment
# download miniconda
if [ "$conda_exists" == "F" ]; then
    echo Downloading and installing Miniconda.
    echo "Downloading Miniconda from $MINICONDA_DOWNLOAD_URL to $INSTALL_DIR/miniconda_installer.sh"

    mkdir -p "$INSTALL_DIR"
    curl -Lk "$MINICONDA_DOWNLOAD_URL" > "$INSTALL_DIR/miniconda_installer.sh"

    chmod u+x "$INSTALL_DIR/miniconda_installer.sh"
    bash "$INSTALL_DIR/miniconda_installer.sh" -b -p $CONDA_ROOT_PREFIX

    # test the conda binary
    echo "Miniconda version:"
    "$CONDA_ROOT_PREFIX/bin/conda" --version
fi

# Environment isolation
export PYTHONNOUSERSITE=1
unset PYTHONPATH
unset PYTHONHOME
export CUDA_PATH="$CONDA_ROOT_PREFIX"
export CUDA_HOME="$CUDA_PATH"

source $CONDA_ROOT_PREFIX/etc/profile.d/conda.sh && conda activate $CONDA_ROOT_PREFIX

$CONDA_ROOT_PREFIX/bin/pip install -r requirements.txt
$CONDA_ROOT_PREFIX/bin/pip install -r custom_requirements.txt
$CONDA_ROOT_PREFIX/bin/python update_data.py

