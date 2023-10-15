# translator.py
import yaml
import re
import os
import sys
from pathlib import Path
import logging

def load_config():
    with open('settings.yml', 'r') as f:
        config = yaml.safe_load(f)
    return config

config = load_config()

def model_exists(language_pair):
    """Check if a model for the language pair exists."""
    model_filename = f"translate-{language_pair}.argosmodel"
    model_path = custom_path / "argos-translate" / "downloads" / model_filename
    return model_path.is_file()

def translation_possible(src, tgt):
    """Check if direct or indirect translation is possible."""
    direct = model_exists(f"{src}_{tgt}")
    indirect = model_exists(f"{src}_en") and model_exists(f"en_{tgt}")
    return direct or indirect

# Define the custom path
script_location = Path(os.path.abspath(sys.argv[0])).parent
custom_path = script_location / "translation_models"

# Ensure the custom path exists
custom_path.mkdir(parents=True, exist_ok=True)

# Set custom paths for Argos Translate
os.environ["XDG_DATA_HOME"] = str(custom_path)
os.environ["XDG_CACHE_HOME"] = str(custom_path)
os.environ["ARGOS_PACKAGES_DIR"] = str(custom_path / "packages")


import argostranslate.package
import argostranslate.translate


# Checks and ensures any needed models used for input translation are downloaded.
if config['translation']['enable']:
    if config['translation']['input_intent_detection'] or config['translation']['all_input']:
        from_code = config['translation']['from_language']
        to_code = config['translation']['to_language']

        # Check if necessary translation models are available
        if not translation_possible(from_code, to_code):
            # Download and install Argos Translate package
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
                ), None  # Return None if not found
            )
            # Check if a package was found before attempting download and install
            if package_to_install:
                argostranslate.package.install_from_path(package_to_install.download())


# Checks and ensures any needed models used for output translation are downloaded. It reverses the to/from languages for the use with the message output.
if config['translation']['enable']:
    if config['translation']['all_output']:
        from_code = config['translation']['to_language']
        to_code = config['translation']['from_language']

        # Check if necessary translation models are available
        if not translation_possible(from_code, to_code):
            # Download and install Argos Translate package
            argostranslate.package.update_package_index()
            available_packages = argostranslate.package.get_available_packages()
            package_to_install = next(
                filter(
                    lambda x: x.from_code == from_code and x.to_code == to_code, available_packages
                ), None  # Return None if not found
            )
            # Check if a package was found before attempting download and install
            if package_to_install:
                argostranslate.package.install_from_path(package_to_install.download())

def translate_message(message):
    """
    Process a users input message and determines if translation is required, and if so returns the translated result.

    Args:
        message (str): The user message to be processed.

    Returns:
        Message: Either the translated message, or the original message if no translation was required.
    """

    # Check if translation is enabled in the config
    if config['translation']['enable']:
        if config['translation']['input_intent_detection'] or config['translation']['all_input']:
            from_code = config['translation']['from_language']
            to_code = config['translation']['to_language']

            # Extract all substrings in double quotes
            quoted_substrings = re.findall(r'"([^"]*)"', message)

            # Replace the quoted substrings with placeholders
            for i, substring in enumerate(quoted_substrings):
                message = message.replace(f'"{substring}"', f'{{quote{i}}}')
            
            # Translate the message
            translated_message = argostranslate.translate.translate(message, from_code, to_code)

            # Replace the placeholders with the original quoted substrings
            for i, substring in enumerate(quoted_substrings):
                translated_message = translated_message.replace(f'{{quote{i}}}', substring)
            
            return translated_message
        else:
            return message
    else:
        return message
        
def translate_output(message):
    """
    Process a users output message and determines if translation is required, and if so returns the translated result.

    Args:
        message (str): The user message to be processed.

    Returns:
        Message: Either the translated message, or the original message if no translation was required.
    """

    if config['translation']['enable']:
        if config['translation']['all_output']:
            from_code = config['translation']['to_language']
            to_code = config['translation']['from_language']

            logging.debug(f"Translate output function called: {message}")

            # Check for the special phrase "Please type 'yes' or 'no':"
            if message == "Please type 'yes' or 'no':":
                # Translate but keep 'yes' and 'no' intact
                part1 = argostranslate.translate.translate("Please type '", from_code, to_code)
                part2 = argostranslate.translate.translate("' or '", from_code, to_code)
                translated_message = f"{part1}yes{part2}no':"
                logging.debug(f"Translated message: {translated_message}")
                return translated_message

            # Check for the special phrase "You may type /cancel to cancel this operation"
            elif "You may type /cancel to cancel this operation" in message:
                # Translate but keep '/cancel' intact
                part1 = argostranslate.translate.translate("You may type ", from_code, to_code)
                part2 = argostranslate.translate.translate(" to cancel this operation", from_code, to_code)
                translated_message = f"{part1} /cancel {part2}"
                
                logging.debug(f"Original message: {message}")
                logging.debug(f"Translated message: {translated_message}")
                return translated_message

            else:
                # Log pre-translation message and translation details
                logging.debug(f"Pre-translation message: {message}")
                logging.debug(f"Translating from: {from_code} to: {to_code}")

                # Default translation if no special phrase is found
                logging.debug(f"Translated message: {message}")
                return argostranslate.translate.translate(message, from_code, to_code)
        else:
            logging.debug(f"No translation (all_output disabled): {message}")
            return message
    else:
        logging.debug(f"No translation (translation disabled): {message}")
        return message
