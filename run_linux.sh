#!/bin/bash

# Get the directory of the script
script_dir="$(dirname "$(readlink -f "$0")")"

# Path to your run_linux.sh script
run_script="./verbose_linux.sh"

# Change the working directory to the script's directory
cd "$script_dir"

# Run the script in the background
nohup /bin/bash "$run_script" > /dev/null 2>&1 &
