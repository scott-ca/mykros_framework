#!/bin/bash

# Path to the desktop file
desktop_file="$HOME/.config/autostart/mykros.desktop"

# Get the current directory of the script
script_directory="$(dirname "$(readlink -f "$0")")"

# Check if the autostart directory exists, and create it if needed
autostart_dir="$HOME/.config/autostart"
if [ ! -d "$autostart_dir" ]; then
    mkdir -p "$autostart_dir"
fi

# Content for the desktop file
desktop_content="[Desktop Entry]
Type=Application
Exec=/bin/bash \"$script_directory/run_linux.sh\"
Hidden=false
NoDisplay=false
Name=Mykros framework
Comment=Used to start up Mykros with your computer"

# Write the content to the desktop file
echo "$desktop_content" > "$desktop_file"

echo "Desktop file created at: $desktop_file"
