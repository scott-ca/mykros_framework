from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import os
import platform
import subprocess

import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info

def example_mute_computer_execution(output_widget, entities, chat_prompt):
    """
    Used for testing actions without training data

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    output_widget.append(f"AI: Test example from mute computer")
