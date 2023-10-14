# translator.py
import yaml
import re
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

import os
import sys
from pathlib import Path

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

# Check if translation is enabled in the config
if config['translation']['enable']:
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
  
    # Translate
    def translate_message(message):
        return argostranslate.translate.translate(message, from_code, to_code)
else:
    def translate_message(message):
        return message  # No translation, return message as is
