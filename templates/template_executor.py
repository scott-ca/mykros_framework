from PySide2.QtWidgets import QDialog, QLabel, QPushButton, QVBoxLayout, QApplication, QWidget
from PySide2.QtCore import QTimer
import os
import platform
import subprocess

import logging

if platform.system() == "Windows":
    import winreg

from util.misc import request_additional_info

def debug_execution(output_widget, entities, chat_prompt):
    """
    Template action

    Args:
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.
        entities (dict): The entities extracted from the user input.
        chat_prompt (ChatPrompt): The ChatPrompt instance used for interacting with the user.
    """

    print("Test")      

