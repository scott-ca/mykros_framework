from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget
from PySide2.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox, QTextEdit, QDialog, QApplication, QStyle

import sys
import os
import yaml
import subprocess
import shutil
import logging


class CustomActionsWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Custom Actions')
        self.resize(1100, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Create a table widget with columns for each piece of information
        self.table_widget = QTableWidget()
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setColumnCount(5) 
        self.table_widget.setHorizontalHeaderLabels(["Intent", "Action", "Description", "Detailed description", "Enabled"])
        main_layout.addWidget(self.table_widget)

        # Button layout
        button_layout = QHBoxLayout()

        # Create buttons for each action
        self.view_action_button = QPushButton('View Custom Action')
        self.view_training_data_button = QPushButton('View Training Data')
        self.toggle_action_button = QPushButton('Enable/Disable')

        self.retrain_restart_button = QPushButton('Retrain Model and Restart')
        self.retrain_restart_button.clicked.connect(self.trigger_retrain_and_restart)
        
        # Connect buttons to functions
        self.view_action_button.clicked.connect(self.view_custom_action)
        self.view_training_data_button.clicked.connect(self.view_training_data)
        self.toggle_action_button.clicked.connect(self.toggle_action)

        # Set the column widths. These are arbitrary values and can be adjusted to your preference.
        self.table_widget.setColumnWidth(0, 150)  # Intent column
        self.table_widget.setColumnWidth(1, 150)  # Action column
        self.table_widget.setColumnWidth(2, 200)  # Description column
        self.table_widget.setColumnWidth(3, 400)  # Detailed description column
        self.table_widget.setColumnWidth(4, 100)  # Enabled column

        self.table_widget.horizontalHeader().setStretchLastSection(False)

        # Add buttons to the layout
        button_layout.addWidget(self.view_action_button)
        button_layout.addWidget(self.view_training_data_button)
        button_layout.addWidget(self.toggle_action_button)
        button_layout.addWidget(self.retrain_restart_button)

        main_layout.addLayout(button_layout)

        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Populate the table widget with custom actions
        self.load_custom_actions()

    def save_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            QMessageBox.information(self, "Success", "File saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while saving the file: {str(e)}")

    def backup_file(self, file_path, backup_dir):
        try:
            shutil.copy(file_path, backup_dir)
            QMessageBox.information(self, "Success", "File backed up successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while backing up the file: {str(e)}")

    def restore_file(self, file_path, backup_dir, text_widget):
        try:
            # Construct backup file path
            backup_file_path = os.path.join(backup_dir, os.path.basename(file_path))
            if not os.path.exists(backup_file_path):
                QMessageBox.warning(self, "Not Found", "No backup found to restore.")
                return

            shutil.copy(backup_file_path, file_path)
            with open(file_path, 'r') as file:
                content = file.read()
            text_widget.setPlainText(content)
            QMessageBox.information(self, "Success", "File restored from backup.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred while restoring the file: {str(e)}")

    def trigger_retrain_and_restart(self):
        try:

            instructions = (
                "The automatic retraining and restart feature is not yet implemented.\n\n"
                "Please manually run the update_data script to retrain the model. "
                "After the script completes, please restart Mykros."
            )
             
            QMessageBox.information(self, "Feature Not Implemented.", instructions)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An unexpected error occurred: {str(e)}")


    def load_custom_actions(self):
        """
        Load and display the custom actions from the intent_config.yml file.
        """

        # Loading intent_config.yml file
        config_file_path = 'intent_config.yml' 
        with open(config_file_path, 'r') as file:
            config_data = yaml.safe_load(file)

        # Clear the table before adding items
        self.table_widget.setRowCount(0)

        # Add items to the table
        for intent_name, intent_info in config_data.items():
            # Insert a new row at the end of the table
            current_row = self.table_widget.rowCount()
            self.table_widget.insertRow(current_row)

            # Create the table cells
            intent_item = QTableWidgetItem(intent_name)
            action_item = QTableWidgetItem(intent_info.get('action', ''))
            summary_item = QTableWidgetItem(intent_info.get('summary', ''))
            details_item = QTableWidgetItem(intent_info.get('details', ''))
            enabled_item = QTableWidgetItem('Enabled' if intent_info.get('enabled', False) else 'Disabled')


            # Set the items as non-editable
            intent_item.setFlags(intent_item.flags() & ~Qt.ItemIsEditable)
            action_item.setFlags(action_item.flags() & ~Qt.ItemIsEditable)
            summary_item.setFlags(summary_item.flags() & ~Qt.ItemIsEditable)
            details_item.setFlags(details_item.flags() & ~Qt.ItemIsEditable)
            enabled_item.setFlags(enabled_item.flags() & ~Qt.ItemIsEditable)


            # Add the items to the table
            self.table_widget.setItem(current_row, 0, intent_item)
            self.table_widget.setItem(current_row, 1, action_item)
            self.table_widget.setItem(current_row, 2, summary_item)
            self.table_widget.setItem(current_row, 3, details_item)
            self.table_widget.setItem(current_row, 4, enabled_item)

    def view_custom_action(self):
        """
        Method to display the custom_action function for the selected item. This should read the data from the custom_actions folder.
        """
        # Get the selected row. If no row is selected, this value will be -1.
        current_row = self.table_widget.currentRow()

        # Check if a row is selected
        if current_row == -1:
            QMessageBox.warning(self, "No selection", "Please select an action to view its code.")
            return

        # Retrieve the action name from the second column
        action_item = self.table_widget.item(current_row, 1)
        action_name = action_item.text()

        # Trim the word "action_" from the action name
        action_name = action_name.replace('action_', '')

        # Define the base directory for custom actions
        base_dir = 'custom_actions'
        
        # Initialize the variable to store the file path
        file_path = None
        
        # Traverse the directory to find the action's Python file
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                # Construct the file path
                current_file_path = os.path.join(root, file)
                # Print the current file path being checked for debugging purposes
                logging.debug(f"Checking: {current_file_path}")

                if file == f'{action_name}_executor.py':
                    file_path = current_file_path
                    break
            if file_path:
                break

        if file_path:
            print(f"File found: {file_path}")
            with open(file_path, 'r') as file:
                code_content = file.read()

            # Create a dialog to display the code content
            dialog = QDialog()
            dialog.setWindowTitle(f'Code for {action_name} action')
            dialog_layout = QVBoxLayout()

            # Create a text edit widget to show the code
            code_viewer = QTextEdit()
            code_viewer.setPlainText(code_content)

            # Create 'Save', 'Backup', and 'Restore' buttons
            save_button = QPushButton('Save')
            backup_button = QPushButton('Backup')
            restore_button = QPushButton('Restore')

            # Define the backup directory
            backup_dir = 'backups/actions'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # Connect buttons to functions
            save_button.clicked.connect(lambda: self.save_file(file_path, code_viewer.toPlainText()))
            backup_button.clicked.connect(lambda: self.backup_file(file_path, backup_dir))
            restore_button.clicked.connect(lambda: self.restore_file(file_path, backup_dir, code_viewer))

            # Add widgets to the dialog layout
            dialog_layout.addWidget(code_viewer)
            button_layout = QHBoxLayout()
            button_layout.addWidget(save_button)
            button_layout.addWidget(backup_button)
            button_layout.addWidget(restore_button)
            dialog_layout.addLayout(button_layout)

            # Set the dialog layout
            dialog.setLayout(dialog_layout)

            dialog.setGeometry(
                QStyle.alignedRect(
                    Qt.LeftToRight, 
                    Qt.AlignCenter, 
                    dialog.size(), 
                    self.geometry()
                )
                                    )

            # Set a decent size for the dialog
            dialog.resize(800, 600)

            # Show the dialog
            dialog.exec_()
        else:
            print(f"File for action '{action_name}' not found.")


    def view_training_data(self):
        """
        Method to view the training data for the selected action. This should read from the
        training data files located in the 'data/nlu' directory.
        """
        # Get the selected row. If no row is selected, this value will be -1.
        current_row = self.table_widget.currentRow()

        # Check if a row is selected
        if current_row == -1:
            QMessageBox.warning(self, "No selection", "Please select an action to view its training data.")
            return

        # Retrieve the action name from the second column of the selected row
        action_item = self.table_widget.item(current_row, 1)
        action_name = action_item.text()

        # Trim the word "action_" from the action name
        action_name = action_name.replace('action_', '')

        # The path to the nlu data folder and the list of potential subdirectories
        nlu_data_path = 'data/nlu'
        subfolders = ["file_actions", "system_actions", "misc_actions", "web_actions", "word_actions"]

        # Placeholder for the content of the training data
        training_data_content = ""

        # Placeholder for the path of the found training data file
        data_file_path = None

        # Search for the training data file across the subdirectories
        for subfolder in subfolders:
            folder_path = os.path.join(nlu_data_path, subfolder)
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.yml') and action_name in file_name:
                    data_file_path = os.path.join(folder_path, file_name)
                    break
            if data_file_path:
                break

        if data_file_path:
            try:
                with open(data_file_path, 'r') as file:
                    training_data_content = file.read()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"An error occurred while reading the file: {str(e)}")
                return
        else:
            QMessageBox.information(self, "Not Found", f"No training data file found for the action '{action_name}'.")
            return

        if data_file_path:

            # Display the training data in a new window
            data_viewer = QDialog(self)
            layout = QVBoxLayout()

            # Create a text edit widget to show the code
            code_viewer = QTextEdit()
            code_viewer.setPlainText(training_data_content)

            # Create 'Save', 'Backup', and 'Restore' buttons
            save_button = QPushButton('Save')
            backup_button = QPushButton('Backup')
            restore_button = QPushButton('Restore')

            # Define the backup directory
            backup_dir = 'backups/training_data'
            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            # Connect buttons to functions
            save_button.clicked.connect(lambda: self.save_file(data_file_path, code_viewer.toPlainText()))
            backup_button.clicked.connect(lambda: self.backup_file(data_file_path, backup_dir))
            restore_button.clicked.connect(lambda: self.restore_file(data_file_path, backup_dir, code_viewer))

            # Add widgets to the layout, not directly to the dialog
            layout.addWidget(code_viewer)
            button_layout = QHBoxLayout() 
            button_layout.addWidget(save_button)
            button_layout.addWidget(backup_button)
            button_layout.addWidget(restore_button)
            layout.addLayout(button_layout)

            # Set the layout for the data_viewer
            data_viewer.setLayout(layout)

    
            data_viewer.setGeometry(
                QStyle.alignedRect(
                    Qt.LeftToRight, 
                    Qt.AlignCenter, 
                    data_viewer.size(), 
                    self.geometry()
                )
                                    )
            
            data_viewer.resize(800, 600)
            data_viewer.setWindowTitle(f"Training Data for '{action_name}'")

            # Show the dialog
            data_viewer.exec_()
        else:
            QMessageBox.information(self, "Not Found", f"No training data file found for the action '{action_name}'.")

    def toggle_action(self):
        """
        Method to enable or disable the selected action. This will update the 'intent_config.yml'
        """
        # Get the selected row. If no row is selected, this value will be -1.
        current_row = self.table_widget.currentRow()

        # Check if a row is selected
        if current_row == -1:
            QMessageBox.warning(self, "No selection", "Please select an action to toggle.")
            return

        # Retrieve the intent name from the first column of the selected row
        intent_item = self.table_widget.item(current_row, 0)
        intent_name = intent_item.text()

        # Define the path to your intent_config.yml file
        config_file_path = 'intent_config.yml'

        # Placeholder for updated lines
        updated_lines = []

        # Flags to identify the intent and "enabled" property
        in_target_intent = False
        found_enabled = False

        with open(config_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                if intent_name + ":" in line.strip():
                    in_target_intent = True

                if in_target_intent and "enabled:" in line:
                    # Modify the "enabled" value
                    enabled_value = "true" if "false" in line else "false"
                    line = f"  enabled: {enabled_value}\n"
                    found_enabled = True

                updated_lines.append(line)

                # Exit the intent section after modifying the "enabled" value
                if found_enabled and line.strip() == "":
                    in_target_intent = False
                    found_enabled = False

        # Write the updated lines back to the file
        with open(config_file_path, 'w') as file:
            file.writelines(updated_lines)

        # Update the table to reflect the change
        self.load_custom_actions()