from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import os
import platform
import subprocess

import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info

def example_open_app_execution(output_widget, entities, chat_prompt):
    """
    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    if "example_open_app_id" in entities:
        example_open_app_id = entities.get("example_open_app_id")
    else:
        # prompt the user for the open_app_id entity
        example_open_app_id = request_additional_info(chat_prompt, "Enter the example software name for this example(No software will be launched, this is just an example):")

        # Check if the user would like to cancel the operation when prompted for additional information
        if example_open_app_id is None:
            output_widget.append("Open application operation canceled.")
            return

    output_widget.append(f"AI: Test example action from open app with entity {example_open_app_id}")
