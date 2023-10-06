import os
import sys
import winshell
import win32com.client

# Get the source and destination paths
script_dir = os.path.dirname(os.path.abspath(__file__))
shortcut_path = os.path.join(script_dir, 'run_windows.vbs')
startup_folder = winshell.startup()

try:
    # Create a shortcut to the file in the startup folder
    shortcut = winshell.CreateShortcut(
        Path=os.path.join(startup_folder, 'mykros_framework.lnk'),
        Target=shortcut_path,
        Icon=(shortcut_path, 0),
        Description='mykros framework'
    )

    # Modify the shortcut's working directory
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut_path = os.path.join(startup_folder, 'mykros_framework.lnk')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.WorkingDirectory = script_dir
    shortcut.Save()

    print('Shortcut created in the startup folder')
except Exception as e:
    print(f'Error occurred while creating the shortcut: {str(e)}')
    sys.exit(1)

