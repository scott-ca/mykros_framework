import os
import yaml
import sys
import shutil
import subprocess
import logging

logging.basicConfig(level=logging.DEBUG)

print("Checking and updating model and intent information.")

# The path to the nlu folder and disabled_nlu_folder
nlu_folder = 'data/nlu'
disabled_nlu_folder = 'disabled_data/disabled_nlu'

# The list of intent folders within the nlu folder
intent_folders = ["file_actions", "system_actions", "misc_actions", "web_actions", "word_actions"]

# The dictionary to store the intents within the intent folders as keys and their respective files as values
intent_dict = {}
disabled_intent_dict = {}

# Iterate through the intent folders in nlu_folder and store the folder paths
for folder in intent_folders:
    folder_path = os.path.join(nlu_folder, folder)
    
    # Get the yml files within the intent folder
    files = [f[:-4] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.yml')]
        
    # Add the intents and their files to the intent_dict
    for file in files:
        intent = os.path.join(folder, file)
        if intent in intent_dict:
            intent_dict[intent].append(folder_path)
        else:
            intent_dict[intent] = [folder_path]

# Printing out all the intents in the intent folders
logging.debug('Intents:')
for intent, locations in intent_dict.items():
    logging.debug(f'{intent}:')
    for location in locations:
        logging.debug(f'- {location}')

# Iterate through the intent folders in disabled_nlu_folder and store the folder paths
for folder in intent_folders:
    folder_path = os.path.join(disabled_nlu_folder, folder)
    
    # Get the yml files within the intent folder
    files = [f[:-4] for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f)) and f.endswith('.yml')]
        
    # Add the intents and their files to the disabled_intent_dict
    for file in files:
        intent = os.path.join(folder, file)
        if intent in disabled_intent_dict:
            disabled_intent_dict[intent].append(folder_path)
        else:
            disabled_intent_dict[intent] = [folder_path]

# Printing out all the intents in the disabled intent folders
logging.debug('\nDisabled Intents:')
for intent, locations in disabled_intent_dict.items():
    logging.debug(f'{intent}:')
    for location in locations:
        logging.debug(f'- {location}')


# Load the intents from the yaml file
with open('intent_config.yml', 'r') as file:
    intents = yaml.safe_load(file)

# Lists to store the enabled and disabled intents
enabled_intents = []
disabled_intents = []

# Comparing intents in yaml with the intents from directory
for intent_name, intent_info in intents.items():
    action = intent_info.get('action')
    if action:
        if intent_info.get('enabled') == True:
            enabled_intents.append({'intent': intent_name, 'action': action})
        else:
            disabled_intents.append({'intent': intent_name, 'action': action})

logging.debug('\nEnabled Intents in config:')
for intent in enabled_intents:
    logging.debug(f'- {intent}')

logging.debug('\nDisabled Intents in config: \n')
for intent in disabled_intents:
    logging.debug(f'- {intent}')

# Check for duplicate intents across all folders
all_intents = list(intent_dict.keys()) + list(disabled_intent_dict.keys())
duplicate_intents = set()

# Find duplicate intents within the nlu folder
for intent, locations in intent_dict.items():
    intent_name = intent.split(os.path.sep)[-1]
    for other_intent in intent_dict:
        other_intent_name = other_intent.split(os.path.sep)[-1]
        if intent_name == other_intent_name and intent != other_intent:
            duplicate_intents.add(intent)
            duplicate_intents.add(other_intent)
            print(f'Duplicate intent {intent_name} found in the nlu folder:')
            for location in locations:
                print(f'- {location}')

# Find duplicate intents within disabled_nlu_folder
for intent, locations in disabled_intent_dict.items():
    intent_name = intent.split(os.path.sep)[-1]
    for other_intent in disabled_intent_dict:
        other_intent_name = other_intent.split(os.path.sep)[-1]
        if intent_name == other_intent_name and intent != other_intent:
            duplicate_intents.add(intent)
            duplicate_intents.add(other_intent)
            print(f'Duplicate intent {intent_name} found in disabled_nlu_folder:')
            for location in locations:
                print(f'- {location}')


# Find duplicate intents within different nlu folders
for intent, locations in intent_dict.items():
    intent_name = intent.split(os.path.sep)[-1]
    for other_intent, other_locations in disabled_intent_dict.items():
        other_intent_name = other_intent.split(os.path.sep)[-1]
        if intent_name == other_intent_name:
            duplicate_intents.add(intent)
            duplicate_intents.add(other_intent)
            print(f'Duplicate intent {intent_name} found between nlu_folder and disabled_nlu_folder:')
            for location in locations:
                print(f'- {location}')
            for other_location in other_locations:
                print(f'- {other_location}')


# Check if duplicate intents were found
if duplicate_intents:
    print('\nDuplicate intents detected. Exiting...')
    sys.exit()


models_dir = os.path.join('models')
model_files = os.listdir(models_dir)


if not model_files:
    print("No files found in the models directory.")
    folder_empty = True
else:
    folder_empty = False
    
    print("\nintent_dict")
    print(intent_dict)
    print("\nenabled_intents")
    print(enabled_intents)
    print("\ndisabled_intent_dict")
    print(disabled_intent_dict)
    print("\ndisabled_intents")
    print(disabled_intents)
    
    print("The following files were found in the models directory:\n")
    for file in model_files:
        print(file)

    confirm = input("\nDo you want to delete these files to re-train the model with the enabled intents? (yes/no): ")

    if confirm.lower() == 'yes' or confirm.lower() == 'y':
        print("Files deletion confirmed.")
        print("Moving files based on intents...\n")

        for file in model_files:
            file_path = os.path.join(models_dir, file)
            os.remove(file_path)
        folder_empty = True
    else:
        print("Files deletion cancelled.")
        sys.exit()

if folder_empty == True:

    # Move disabled intents from nlu_folder to disabled_nlu_folder if needed
    for intent, locations in intent_dict.items():
        intent_name = intent.split(os.path.sep)[-1]
        if intent_name in [item['intent'] for item in disabled_intents]:
            for location in locations:
                source_file = os.path.join(location, intent.split('/')[-1] + '.yml')
                destination_folder = os.path.join(disabled_nlu_folder, os.path.basename(location))
                destination_file = os.path.join(destination_folder, intent.split('/')[-1] + '.yml')
                if os.path.exists(source_file):
                    print(f"Moving '{source_file}' to '{destination_file}'")
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(source_file, destination_file)
                else:
                    print(f"Source file '{source_file}' not found. Skipping...")

    # Move enabled intents from disabled_nlu_folder to nlu_folder if needed
    for intent, locations in disabled_intent_dict.items():
        intent_name = intent.split(os.path.sep)[-1]
        if intent_name in [item['intent'] for item in enabled_intents]:
            for location in locations:
                source_file = os.path.join(location, intent.split('/')[-1] + '.yml')
                destination_folder = os.path.join(nlu_folder, os.path.basename(location))
                destination_file = os.path.join(destination_folder, intent.split('/')[-1] + '.yml')

                if os.path.exists(source_file):
                    print(f"Moving '{source_file}' to '{destination_file}'")
                    os.makedirs(destination_folder, exist_ok=True)
                    shutil.move(source_file, destination_file)
                else:
                    print(f"Source file '{source_file}' not found. Skipping...")

    print("\nIntents moved successfully.")


# Generate rules.yml content
rules_content = f"version: '3.1'\n\nrules:\n"
for intent in enabled_intents:
    action = intent["action"]
    rule_name = intent["intent"].replace('_', ' ').capitalize()
    rules_content += f"- rule: {rule_name}\n"
    rules_content += "  steps:\n"
    rules_content += f"  - intent: {intent['intent']}\n"
    rules_content += f"  - action: {action}\n"
    rules_content += "\n"

# Generate stories.yml content
stories_content = f"version: '3.1'\n\nstories:\n"
stories_content += "- story: General Management\n"
stories_content += "  steps:\n"
for intent in enabled_intents:
    stories_content += f"  - intent: {intent['intent']}\n"
    stories_content += f"  - action: {intent['action']}\n"
stories_content += "\n"

# Define the file paths for rules.yml and stories.yml
rules_file_path = os.path.join('data', 'rules.yml')
stories_file_path = os.path.join('data', 'stories.yml')

# Write rules.yml
with open(rules_file_path, 'w') as file:
    file.write(rules_content)

# Write stories.yml
with open(stories_file_path, 'w') as file:
    file.write(stories_content)

print("Files 'rules.yml' and 'stories.yml' configuration created successfully.")

print("Training the rasa model")

# Command to run Rasa
rasa_command = ['rasa', 'train']

# Run Rasa and capture the output live
process = subprocess.Popen(rasa_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

# Read and print the output line by line for the training of the model
for line in process.stdout:
    print(line, end='')

# Wait for the process to finish
process.wait()