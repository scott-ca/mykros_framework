#!/bin/bash

# Config
CONDA_ROOT_PREFIX="$(pwd)/portable_env/conda"

# environment isolation
export PYTHONNOUSERSITE=1
unset PYTHONPATH
unset PYTHONHOME
export CUDA_PATH="$CONDA_ROOT_PREFIX"
export CUDA_HOME="$CUDA_PATH"

source $CONDA_ROOT_PREFIX/etc/profile.d/conda.sh && conda activate $CONDA_ROOT_PREFIX

$CONDA_ROOT_PREFIX/bin/python mykros_framework.py
