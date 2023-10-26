import subprocess
import sys
import os
import platform

def main():
    # Directory adjustments
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # This navigates up one directory

    # Step 1: Assumption is made that the main script is already stopped.

    # Step 3: Restart your shell script based on the operating system
    os_name = platform.system()

    # Step 2: Run your intermediate script
    try:
        # Using the same Python interpreter to run the intermediate script

        if os_name == "Linux":
            intermediate_script = os.path.join(parent_dir, 'update_data.sh')
            subprocess.check_call(['/bin/bash', intermediate_script, '--auto'])

        elif os_name == "Windows":
            intermediate_script = os.path.join(parent_dir, 'update_data.bat')
            subprocess.check_call([intermediate_script, '--auto'], shell= True)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running {intermediate_script}: {e}")
        sys.exit(1)  # Exit if the call was unsuccessful


    try:

        if os_name == "Linux":
            script_to_restart = os.path.join(parent_dir, 'run_linux.sh')
            subprocess.check_call(['/bin/bash', script_to_restart])

        elif os_name == "Windows":
            script_to_restart = os.path.join(parent_dir, 'run_windows.vbs')
            subprocess.check_call([script_to_restart], shell= True)

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while trying to restart the script: {e}")
        sys.exit(1)  # Exit if the call was unsuccessful

if __name__ == "__main__":
    main()
