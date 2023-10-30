from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QTableWidget, QFileDialog
from PySide2.QtWidgets import QTableWidgetItem, QAbstractItemView, QMessageBox, QTextEdit, QDialog, QApplication, QStyle
from collections import OrderedDict
import zipfile
import tempfile
import sys
import os
import yaml
import subprocess
import shutil
import logging
import re


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
        self.import_button = QPushButton('Import Custom Action')
        self.export_button = QPushButton('Export Custom Action')
        
        # Connect buttons to functions
        self.view_action_button.clicked.connect(self.view_custom_action)
        self.view_training_data_button.clicked.connect(self.view_training_data)
        self.toggle_action_button.clicked.connect(self.toggle_action)
        self.import_button.clicked.connect(self.import_custom_action)
        self.export_button.clicked.connect(self.export_custom_action)

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
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.export_button)

        main_layout.addLayout(button_layout)

        # Set the main layout
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Populate the table widget with custom actions
        self.load_custom_actions()

    def import_custom_action(self):
        """
        Used to import an intent and their respective action. This will include the custom_action, training data, and the intent_config, domain details.
        It will open a dialog box and accept a zip file with the files in the structure of where the files normally reside.
        """

        # Step 1: Select and open the ZIP file
        import_path, _ = QFileDialog.getOpenFileName(self, "Select the custom action Zip file", "", "Zip files (*.zip)")
        if not import_path:
            QMessageBox.warning(self, "No File Selected", "No file was selected.")
            return

        # Step 2: Extract to a temporary location
        temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(import_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Creates paths based on the expected structure
        project_base_path = '.'
        base_action_path = os.path.join(project_base_path, 'custom_actions')
        base_training_path = os.path.join(project_base_path, 'data', 'nlu')
        intent_config_path = os.path.join(project_base_path, 'intent_config.yml')

        # Function to handle checking and copying files
        def check_and_copy(source, destination, file_description):
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(destination), exist_ok=True)

            if os.path.exists(destination):
                # Conflict detected: Prompt the user
                choice = QMessageBox.question(self, "Conflict Detected",
                                            f"The {file_description} already exists. Do you want to overwrite it?",
                                            QMessageBox.Yes | QMessageBox.No,
                                            QMessageBox.No)
                if choice == QMessageBox.No:
                    return False  # Skip this file

            # Copy the file
            shutil.copy2(source, destination)
            return True

        files_imported = 0
        try:
            # Check each file for conflicts, and copy over
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    full_file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_file_path, temp_dir)

                    # Normalize the path to ensure cross-platform compatibility
                    normalized_rel_path = os.path.normpath(rel_path)

                    # Determine the destination path based on the normalized relative path
                    if normalized_rel_path.startswith(os.path.normpath('custom_actions')):
                        dest_path = os.path.join(base_action_path, os.path.relpath(normalized_rel_path, 'custom_actions'))
                    elif normalized_rel_path.startswith(os.path.normpath('data/nlu')):
                        dest_path = os.path.join(base_training_path, os.path.relpath(normalized_rel_path, 'data/nlu'))
                    else:
                        continue

                    # Copy file, handle conflicts
                    if check_and_copy(full_file_path, dest_path, file_description=file):
                        files_imported += 1

            # Handling 'intent_config.yml'
            temp_intent_config = os.path.join(temp_dir, 'intent_config.yml')
            if os.path.isfile(temp_intent_config):
                with open(temp_intent_config, 'r') as temp_intent_stream:
                    temp_intents = yaml.safe_load(temp_intent_stream)

                with open(intent_config_path, 'r') as main_intent_stream:
                    main_intents = yaml.safe_load(main_intent_stream) or {}

                # Merge intents, prompt for overwrite if there's a conflict
                updated_intents = main_intents.copy()
                for intent_name, intent_data in temp_intents.items():
                    if intent_name in main_intents:
                        # Conflict: Prompt the user
                        choice = QMessageBox.question(self, "Conflict Detected",
                                                    f"The intent '{intent_name}' already exists in intent_config. Do you want to overwrite it?",
                                                    QMessageBox.Yes | QMessageBox.No,
                                                    QMessageBox.No)
                        if choice == QMessageBox.No:
                            continue  # Skip this intent

                    # Add or update the intent
                    updated_intents[intent_name] = intent_data

                # Save back to 'intent_config.yml'
                with open(intent_config_path, 'w') as main_intent_stream:
                    first_entry = True
                    for intent, data in updated_intents.items():
                        yaml_content = yaml.dump({intent: data}, default_flow_style=False, sort_keys=False)

                        # If it's not the first entry, we prepend a newline to separate the intents
                        if not first_entry:
                            yaml_content = '\n' + yaml_content
                        else:
                            first_entry = False

                        main_intent_stream.write(yaml_content)


            # Extracting new intent and action names after the merge
            new_intent_names = list(updated_intents.keys())  # Extracting all the intent names

            new_action_names = []
            for intent_data in updated_intents.values():
                if 'action' in intent_data:
                    action_name = intent_data['action']
                    if action_name not in new_action_names:
                        new_action_names.append(action_name)

            # Define the paths for domain files
            temp_domain_path = os.path.join(temp_dir, 'domain.yml')
            domain_path = os.path.join(project_base_path, 'domain.yml')

            # Handle 'domain.yml' with the new intent and action names, as well as entities
            if os.path.isfile(temp_domain_path):
                with open(temp_domain_path, 'r') as temp_domain_stream:
                    temp_domain_data = yaml.safe_load(temp_domain_stream)

                with open(domain_path, 'r') as domain_stream:
                    domain_data = yaml.safe_load(domain_stream) or {}

                # Add new intents to the domain file if they don't exist
                existing_intents = domain_data.get('intents', [])
                for intent_name in new_intent_names:
                    if intent_name not in existing_intents:
                        existing_intents.append(intent_name)

                # Add new actions to the domain if they don't exist
                existing_actions = domain_data.get('actions', [])
                for action_name in new_action_names:
                    if action_name not in existing_actions:
                        existing_actions.append(action_name)

                domain_data['intents'] = existing_intents  # Updating with new intents list
                domain_data['actions'] = existing_actions  # Updating with new actions list

                # Handling entities from the imported 'domain.yml'
                if 'entities' in temp_domain_data:
                    temp_entities = temp_domain_data['entities']
                    updated_entities = domain_data.get('entities', []).copy()

                    # Check for entity conflicts
                    for temp_entity in temp_entities:
                        entity_name = temp_entity if isinstance(temp_entity, str) else list(temp_entity.keys())[0]

                        # Search for the entity in the current domain file
                        conflict = False
                        for index, entity in enumerate(updated_entities):
                            existing_entity_name = entity if isinstance(entity, str) else list(entity.keys())[0]

                            if entity_name == existing_entity_name:
                                conflict = True

                                # Conflict: Prompt the user
                                choice = QMessageBox.question(self, "Conflict Detected",
                                                            f"The entity '{entity_name}' already exists in domain.yml. Do you want to overwrite it?",
                                                            QMessageBox.Yes | QMessageBox.No,
                                                            QMessageBox.No)
                                if choice == QMessageBox.Yes:
                                    updated_entities[index] = temp_entity  # Replace the entity with the imported one
                                break

                        if not conflict:
                            # If no conflict was found, add the new entity
                            updated_entities.append(temp_entity)

                    domain_data['entities'] = updated_entities  # Updating with the new entities list

                # Prepare data for dumping in the correct order
                ordered_keys = ["version", "intents", "actions", "entities", "session_config"]
                ordered_domain_data = {key: domain_data[key] for key in ordered_keys if key in domain_data}


                # Serialize each section separately, as you've done before
                yaml_sections = []
                for key in ordered_keys:
                    if key in domain_data:
                        section_yaml = yaml.dump({key: domain_data[key]}, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)
                        yaml_sections.append(section_yaml)

                full_yaml = '\n'.join(yaml_sections)

                # Write the updated domain data back to 'domain.yml'
                with open(domain_path, 'w') as domain_stream:
                    domain_stream.write(full_yaml)

            # Clean up the temporary directory
            shutil.rmtree(temp_dir)

            # Reload custom actions list in main window.
            self.load_custom_actions()

            # Inform the user of the import status
            QMessageBox.information(self, "Import Successful", f"Custom action import completed. {files_imported} items were imported.")
        except Exception as e:
            # Removing temp directory
            shutil.rmtree(temp_dir)
            QMessageBox.critical(self, "Import Failed", f"An error occurred during the import: {str(e)}")


    def export_custom_action(self):
        """
        Used to export an intent and their respective action. This will include the custom_action, training data, and the intent_config and domain details.
        It will open a dialog box and take a file name and directory as an input of where to store the zip file.
        """

        # Get all selected rows
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select one or more custom actions to export.")
            return

        # Variables for directories

        script_dir = os.path.dirname(os.path.realpath(__file__))
        base_action_dir = 'custom_actions'
        base_training_dir = 'data/nlu'
        action_folders = ["file_actions", "system_actions", "misc_actions", "web_actions", "word_actions"]

        # Lists to store collective data
        all_action_files = set()
        all_training_data = set()
        all_related_entities = set()
        all_intent_configs = []

        for index in selected_rows:
            current_row = index.row()

            # Retrieve the intent and action names from the table widget
            intent_item = self.table_widget.item(current_row, 0)
            intent_name = intent_item.text()

            action_item = self.table_widget.item(current_row, 1)

             # Trim the 'action_' prefix
            action_name = action_item.text().replace('action_', '') 

            # Initialize paths and lists for this specific action
            action_files = set()
            relative_action_paths = set()

            # Check each folder for action files
            for folder in action_folders:
                folder_path = os.path.join(base_action_dir, folder, action_name)
                if os.path.isdir(folder_path):
                    for file in os.listdir(folder_path):
                        file_path = os.path.join(folder_path, file)
                        action_files.add((file_path, os.path.relpath(file_path, base_action_dir)))
                    if action_files:
                        break  

            # Store action files in the main list
            all_action_files.update(action_files)

            # Construct the path for the training data and find the training file
            training_data_path = None
            relative_training_path = None
            for subfolder in action_folders:
                folder_path = os.path.join(base_training_dir, subfolder)
                if os.path.isdir(folder_path):
                    for file in os.listdir(folder_path):
                        if file.endswith('.yml') and action_name in file:
                            training_data_path = os.path.join(folder_path, file)
                            relative_training_path = os.path.relpath(training_data_path, base_training_dir)
                            break
                    if training_data_path:
                        break

            # If a training data file was found, add it to the list
            if training_data_path:
                all_training_data.add((training_data_path, relative_training_path))

            # Extract entities from this training data file
            with open(training_data_path, 'r') as td_file:
                td_content = yaml.safe_load(td_file)
                for item in td_content['nlu']:
                    if 'intent' in item and item['intent'] == intent_name:
                        examples = item.get('examples', '').split('\n')
                        for ex in examples:
                            matches = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', ex)
                            for _, entity in matches:
                                all_related_entities.add(entity)
                    
            # Read the intent_config.yml and extract the specific intent's configuration
            intent_config_content = None
            with open('intent_config.yml', 'r') as stream:
                try:
                    documents = yaml.safe_load(stream)
                    if intent_name in documents:
                        intent_data = documents[intent_name]
                        intent_config_content = yaml.dump({intent_name: intent_data}, default_flow_style=False, sort_keys=False)
                except yaml.YAMLError as exc:
                    QMessageBox.critical(self, "Error", f"An error occurred reading the intent_config.yml: {str(exc)}")
                    return

            if intent_config_content:
                all_intent_configs.append((intent_name, intent_config_content))

        # Extract the related entity details from domain.yml
        domain_file_path = os.path.join(script_dir, 'domain.yml')
        domain_entity_data = []
        with open('domain.yml', 'r') as domain_file:
            domain_content = yaml.safe_load(domain_file)
            for entity_spec in domain_content.get('entities', []):
                entity_name = entity_spec  
                if isinstance(entity_spec, dict):

                    entity_name = list(entity_spec.keys())[0]
                    
                # Check if the entity is in our list of related entities
                if entity_name in all_related_entities:
                    domain_entity_data.append(entity_spec)

        # After gathering all necessary files and configurations, proceeds with the ZIP creation
        try:
            export_name = "multiple_intents" if len(selected_rows) > 1 else intent_name
            export_path = QFileDialog.getSaveFileName(self, 'Save File', f"{export_name}.zip", "Zip files (*.zip)")
            if export_path[0]:
                with zipfile.ZipFile(export_path[0], 'w') as export_zip:
                    # Adding custom action script(s) and training data
                    for file_info in all_action_files:
                        file_path, rel_path = file_info
                        full_zip_action_path = os.path.join('custom_actions', rel_path)
                        export_zip.write(file_path, full_zip_action_path)

                    for data_info in all_training_data:
                        data_path, rel_path = data_info
                        full_zip_training_path = os.path.join('data', 'nlu', rel_path)
                        export_zip.write(data_path, full_zip_training_path)

                    if domain_entity_data:
                        domain_content_str = yaml.dump({"entities": domain_entity_data}, default_flow_style=False, sort_keys=False)
                        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_domain:
                            temp_domain.write(domain_content_str)
                            temp_domain_path = temp_domain.name
                        export_zip.write(temp_domain_path, 'domain.yml')
                        os.remove(temp_domain_path)  # Clean up the temp file

                    # Combine all intent configurations into one content
                    combined_intent_config = {}
                    for intent_info in all_intent_configs:
                        intent_name, intent_content = intent_info
                        # Parses the individual YAML content back to a dictionary and merges it.
                        intent_data = yaml.safe_load(intent_content)
                        combined_intent_config.update(intent_data)

                    # Dump all intent data into one YAML configuration
                    if combined_intent_config:
                        all_intents_content = yaml.dump(combined_intent_config, default_flow_style=False, sort_keys=False)

                        # Split the content of the YAML by newlines and add an extra newline for each top-level item
                        adjusted_content_lines = []
                        first_item = True  
                        for line in all_intents_content.split('\n'):
                            if line.endswith(':') and not line.startswith('  '):
                                if not first_item:
                                    adjusted_content_lines.append('')  
                                else:
                                    first_item = False
                            adjusted_content_lines.append(line)

                        # Join everything back together into a single string with the added newlines
                        adjusted_content = '\n'.join(adjusted_content_lines)

                        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_config:
                            temp_config.write(adjusted_content)  
                            temp_config_path = temp_config.name

                        export_zip.write(temp_config_path, 'intent_config.yml')
                        os.remove(temp_config_path)  # Clean up the temp file

                QMessageBox.information(self, "Export Successful", f"Custom actions have been exported successfully.")
            else:
                QMessageBox.warning(self, "Export Cancelled", "The export operation was cancelled.")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"An error occurred during export: {str(e)}")

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
        """
        Calls the restart_actions standalone script and the ends the main Mykros script.
        The restart_actions script will run update_data.py and then re-launch Mykros.
        """
        try:

            restart_script = './util/restart_actions.py'
            subprocess.Popen(['python', restart_script])
            sys.exit(0)
            
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