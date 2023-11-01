import os
import sys
from PySide2 import QtCore
from PySide2.QtWidgets import QLineEdit
from PySide2.QtCore import Signal
from collections import defaultdict
import glob
import re
import yaml
import logging

from util.misc import find_nonwords
from custom_actions.execute_actions import execute_action
from util.misc import intent_help
from util.rasa_model import rasa_model

# Load the YAML configuration file
with open('intent_config.yml', 'r') as stream:
    try:
        intents_config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        logging.debug(exc)

# Filter out the disabled intents and add 'action_intent'
intent_info = {
    imported_intent: {
        **{key: value for key, value in action.items() if key in ['action', 'summary', 'details']}
    } 
    for imported_intent, action in intents_config.items() if action.get('enabled') == True
}

actions = {}  # Initialize an empty dictionary

for intent_name in intent_info.keys():
    action_key = intent_info.get(intent_name, {}).get('action', None)
    
    # Assign the action to the corresponding intent in the dictionary
    actions[intent_name] = action_key

print("intent info:\n")
print(intent_info)

class ChatPrompt(QLineEdit):
    """A custom QLineEdit widget for handling user input in the chat prompt."""

    input_received = Signal(str)

    def __init__(self, output_widget=None):
        """Initialize the ChatPrompt class.

        Args:
            output_widget (QTextEdit, optional): The QTextEdit widget for displaying the chat conversation. Defaults to None.
        """

        super().__init__()
        self.output_widget = output_widget
        self.moveToThread(QtCore.QCoreApplication.instance().thread())
        self.input_received.connect(self._store_input)
        self.expecting_additional_info = False
        self.first_response = True
        self.nlu_data = self.load_nlu_data()
        self.regex_patterns = self.load_regex_patterns()


        if 'DEBUG_MODE' in actions:
            self.output_widget.append(f"**DEBUG MODE ENABLED**.\n\nIF THIS WASN'T INTENTIONALLY ENABLED PLEASE DISABLE IT IN THE intent_config.yml FILE\n")

    def wait_for_input(self):
        """Wait for user input.

        Returns:
            str: The user input.
        """

        loop = QtCore.QEventLoop()
        self.input_received.connect(loop.quit)
        loop.exec_()
        return self._user_input

    def _store_input(self, user_input):
        """Store the user input.

        Args:
            user_input (str): The user input.
        """        
        self._user_input = user_input

    def request_input(self, prompt_text):
        """Request user input with a prompt.

        Args:
            prompt_text (str): The prompt text to display to the user.

        Returns:
            Signal: The input received signal.
        """
        self.output_widget.append(f"AI: {prompt_text}")
        input_received = self.input_received

        def handle_input():
            """ This function is called when the user presses the Return or Enter key
            after entering their input. It retrieves the user's input, emits the
            input received signal, and clears the input field.
            """

            user_input = self.text()
            self.setText('')
            input_received.emit(user_input)

        self.returnPressed.connect(handle_input)
        return input_received

    def keyPressEvent(self, event):
        """Handle key press events.

        Args:
            event (QEvent): The key press event.
        """
        if event.key() == QtCore.Qt.Key_Return or event.key() == QtCore.Qt.Key_Enter:
            self.handle_chat()
        else:
            super().keyPressEvent(event)


    def load_nlu_data(self):
        """pre-loads nlu data."""

        # Specify the directory where the NLU files are located
        nlu_directory = os.path.join(os.getcwd(), "data", "nlu")

        # Initialize an empty dictionary to store the NLU data
        nlu_data_list = {}

        # Specify the subfolder names to search for
        subfolder_names = ["file_actions", "system_actions", "misc_actions", "web_actions", "word_actions" ]

        # Recursively search for .yml file paths in the directory and its subfolders
        for subfolder_name in subfolder_names:
            subfolder_path = os.path.join(nlu_directory, subfolder_name)
            subfolder_files = glob.glob(os.path.join(subfolder_path, "*.yml"))
            for file_path in subfolder_files:
                with open(file_path, "r") as file:
                    nlu_data_temp = yaml.safe_load(file)
                    file_name = os.path.basename(file_path)
                    nlu_data_list[file_name] = nlu_data_temp

        nlu_data = defaultdict(list)

        for data in nlu_data_list.values():
            for key, value in data.items():
                if isinstance(value, list):
                    nlu_data[key].extend(value)
                else:
                    nlu_data[key] = value

        # Replaces the placeholders IE. __FSLASH__,__BSLASH__,__PERCENT__ in the training data with forward slashes so that it can display correctly for the user in the output widget.
        nlu_data = {key: replace_specialchar(value) for key, value in nlu_data.items()}

        logging.debug("\nNLU: Data\n")
        logging.debug(nlu_data)

        return nlu_data
        

    def load_regex_patterns(self):
        """pre-loads regex paterns"""

        # Prepare regex patterns for intent matching
        regex_patterns = prepare_intent_patterns(self.nlu_data)

        logging.debug("Regex Patterns:")
        logging.debug(regex_patterns)
        logging.debug("End of Regex Patterns")

        return regex_patterns

    def handle_chat(self):
        """Handle the user's chat input."""
        
        
        user_input = self.text()
        logging.debug(f"TYPE: {type(user_input)}, CONTENT: {user_input}")

        logging.debug(f"ORIGINAL USER INPUT: {repr(user_input)}")
        self.setText('')
        logging.debug(f"ORIGINAL USER INPUT: {repr(user_input)}")
        if self.first_response == True:
            self.output_widget.append(f"You: {user_input}", bypass_translation=True)


        elif self.first_response == False:
            self.output_widget.append(f"\nYou: {user_input}", bypass_translation=True)
            logging.debug(f"ORIGINAL USER INPUT: {repr(user_input)}")
        if user_input == "/help" or user_input.startswith("/help "):
            if user_input == "/help":
                user_input = "/help general"
            intent_help(user_input, intent_info, self.output_widget)

        else:

            # Get response from Rasa model
            response = rasa_model.message(user_input)
            
            intent_ranking = response["intent_ranking"]

            logging.debug(f"Intents prior to disabled filtering shared actions:\n {intent_ranking}")

            # Filter out intents that are not enabled in the intent_config.yml
            intent_ranking = [intent for intent in intent_ranking if intent["name"] in intent_info]

            logging.debug(f"Intents after disabled filtering shared actions:\n {intent_ranking}")

            logging.debug(response)

            # Load the YAML file for confidence threshold
            with open('settings.yml', 'r') as file:
                settings = yaml.safe_load(file)            

            # Used to control if the translated data goes to the custom_actions.
            translated_user_input = user_input

            if settings['translation']['enable'] is True:
                    if settings['translation']['input_intent_detection'] is True or settings['translation']['all_input'] is True:
                        user_input = response['text']
                        user_input = replace_specialchar(user_input)
                        if settings['translation']['all_input'] is True:
                            translated_user_input = user_input
                

            logging.debug(f"\nInitial response:\n {response}")

            # List of initial entities in the response for debugging
            initial_entities = response.get('entities', [])

            # Log the initial entities
            logging.debug(f"\nInitial entities:\n {initial_entities}")

            # Group entities by entity name
            from collections import defaultdict
            entity_groups = defaultdict(list)
            for entity in response['entities']:
                entity_groups[entity['entity']].append(entity)

            # Determine the best entity for each group
            best_entities = []
            for entity_type, entities in entity_groups.items():

                # Checks if any of the extractions for the entity group come from RegexEntityExtractor. If so, makes it the priority and skips the remaining in the group.
                regex_entities = [e for e in entities if e.get('extractor') == 'RegexEntityExtractor']
                if regex_entities:
                    best_entities.extend(regex_entities)
                    continue

                # Filter out entities without a 'confidence_entity' and sort the rest with lowest being first.
                entities_with_confidence = [e for e in entities if 'confidence_entity' in e]
                entities_with_confidence = sorted(entities_with_confidence, key=lambda x: x['confidence_entity'])

                # If we have entities with confidence scores, set the first one as the current best
                if entities_with_confidence:
                    best_entity = entities_with_confidence[0]
                else:
                    # If there are no entities with confidence scores, just use the first entity in the original list
                    best_entity = entities[0]

                # Iterate and compare
                for entity in entities:
                    current_word_count = word_count(entity['value'])
                    best_word_count = word_count(best_entity['value'])

                    # Check if the current entity has more words or the same number of words but higher confidence and updates accordingly
                    if current_word_count > best_word_count or (current_word_count == best_word_count and entity.get('confidence_entity', 0) > best_entity.get('confidence_entity', 0)):
                        best_entity = entity

                # Add the best entity to the result list
                best_entities.append(best_entity)

            response['entities'] = best_entities


            logging.debug(f"\nTop confidence of each entity:\n {response['entities']}")
                
            # Retrieve the confidence_threshold value for any intents to be considered present in the repsonse.
            confidence_threshold = settings['confidence_threshold']

            # Print the confidence_threshold
            logging.debug(f"Confidence Threshold: {confidence_threshold}")

            if self.expecting_additional_info == False:
                if self.first_response == True:
                    self.first_response = False
                    
            # Updates the intent confidence based on present keywords for the intents in the user input.
            if "nlu_fallback" not in [intent["name"] for intent in intent_ranking]:
                intent_ranking = keyword_confidence_update(intent_ranking, self.regex_patterns, user_input)
                    
            # Filter intents above confidence threshold
            intents_above_threshold = [intent for intent in intent_ranking if intent["confidence"] >= confidence_threshold]

            logging.debug("intent ranking prior to conflict groups:")
            logging.debug(intents_above_threshold)

            
            # Read the YAML file for list of intents that may have a lot of overlap with intent detection.
            with open('conflict_groups.yml', 'r') as file:
                config = yaml.safe_load(file)

            # Access the conflict_groups list from the conflict_groups.yml file
            conflict_groups = [tuple(group['intents']) for group in config['conflict_groups']]
                      
            # Count how many instances of export/exported to determine amount of iterations of the conflict group to bypass to allow linking of intents
            export_count = 0
            export_count = user_input.lower().count("exported")
            export_count += user_input.lower().count("export")

            if export_count == 0:

                # Resolve conflicts within conflict groups based on highest confidence score
                for group in conflict_groups:
                    conflicting_intents = [intent for intent in intents_above_threshold if intent["name"] in group]
                    if len(conflicting_intents) >= 2:
                        highest_confidence_intent = max(conflicting_intents, key=lambda intent: intent["confidence"])
                        intents_above_threshold = [intent for intent in intents_above_threshold if intent not in conflicting_intents]
                        intents_above_threshold.append(highest_confidence_intent)

            else:
 
                # Sorts intents that are above the threshold in descending order and assign the export_count+1 worth of top values to highest_confidence_intents
                highest_confidence_intents = sorted(intents_above_threshold, key=lambda intent: intent["confidence"], reverse=True)[:export_count + 1]

                intents_above_threshold = highest_confidence_intents


            # Logging: Print post conflict_groups filter
            logging.debug("Filtered Intents after conflict_group filter")
            for intent in intents_above_threshold:
                intent_name = intent['name']
                confidence = intent['confidence']
                logging.debug(f"Intent '{intent_name}': Confidence: {confidence}")

            # Logging: Print intent information before sorting
            logging.debug("Before sorting:")
            for index, intent in enumerate(intents_above_threshold):
                position = intent_position(f"{intent['name']}_keywords", user_input, self.regex_patterns)
                logging.debug(f"Intent {index + 1}: {intent['name']}, Position: {position}, Confidence: {intent['confidence']}")

            # Sort intents based on keyword position so that mutliple intents are executed in the correct order
            sorted_intents = sorted(
                intents_above_threshold,
                key=lambda intent: intent_position(f"{intent['name']}_keywords", user_input, self.regex_patterns),
            )

            # Logging: Print intent information after sorting
            logging.debug("\nAfter sorting:")
            for index, intent in enumerate(sorted_intents):
                position = intent_position(f"{intent['name']}_keywords", user_input, self.regex_patterns)
                logging.debug(f"Intent {index + 1}: {intent['name']}, Position: {position}, Confidence: {intent['confidence']}")

            top_intents = sorted_intents

            # Extract keywords from user input
            extracted_keywords = extract_keywords(user_input, self.regex_patterns)
            logging.debug(f"Extracted keywords: {extracted_keywords}")

            # Logging: Print extracted entities and sorted intents
            logging.debug(f"Entities: {response['entities']}")
            logging.debug(f"Sorted Intents: {top_intents}")
            for index, intent in enumerate(top_intents):
                logging.debug(f"Intent {index + 1}: {intent['name']}, Confidence: {intent['confidence']}")

            # Logging: Print regex patterns
            for item in self.nlu_data["nlu"]:
                if "regex" in item:
                    logging.debug(f"Entity '{item['regex']}' has a regex pattern.")
                    
            logging.debug("end of list of intents with patterns")

            # create an empty entities dictionary
            entities = {entity["entity"]: entity["value"] for entity in response["entities"]}
            entities = {key: replace_specialchar(value) for key, value in entities.items()}

            # loop through each entity in the response
            for entity in self.nlu_data["nlu"]:
                if "regex" in entity:
                    # check if the entity exists in the extracted keywords dictionary
                    if entity['regex'] in extracted_keywords:
                        # Makes sure to not replace any pre-existing value. this the only bit added
                        if entity['regex'] in entities and not entities[entity['regex']]:
                            # set the entity value to the corresponding value in the extracted keywords dictionary. Used for custom entity regex extraction. IE. terminal_command or browser.
                            entities[entity['regex']] = extracted_keywords[entity['regex']][0]
                            logging.debug(f"Entity updated for entity: {entity} and with the keyword {entities[entity['regex']]}  ")
                else:
                    logging.debug("no keywords")

            # Logging: Print top intents, entities, response, and intent ranking.
            logging.debug(f"Top Intents: {top_intents}")
            logging.debug(f"Entities: {entities}")
            logging.debug(f"Response: {response}")
            logging.debug(f"Intent Ranking: {intent_ranking}")

            # Check if any of the intents require additional information from the user
            if self.expecting_additional_info:
                self._user_input = translated_user_input
                self.input_received.emit(translated_user_input)
                self.expecting_additional_info = False
                return

            # Check if the top intent is a chat intent and append AI response to output_widget
            if "chat" in [intent["name"] for intent in top_intents]:
                self.output_widget.append(f"AI: {response['text']}")
            else:
                process_intents(self.nlu_data, top_intents, entities, user_input, self.regex_patterns, self.output_widget, self)


def replace_specialchar(value):
    """
    Replaces the various placeholders such as '__FSLASH__' and '__BSLASH__' with their respective special characters.

    Args:
        value (str, list, dict): The value to process.

    Returns:
        str, list, dict: The value of respective special characters for the placeholders.
    """

    if isinstance(value, str):
        value = value.replace("__FSLASH__", "/")
        value = value.replace("__PERCENT__", "%")
        value = value.replace("__BSLASH__", "\\")
        value = value.replace("__DASH__", "-")
        return value
    elif isinstance(value, list):
        return [replace_specialchar(item) for item in value]
    elif isinstance(value, dict):
        return {key: replace_specialchar(item) for key, item in value.items()}
    else:
        return value


def keyword_confidence_update(intent_ranking, regex_patterns, user_input):
    """
    Update the confidence scores of intents based on keyword associations.

    Args:
        intent_ranking (list): A list of intent dictionaries containing 'name' and 'confidence' keys.
        regex_patterns (dict): A dictionary of regular expressions patterns for intent keywords.
        user_input (str): The user input string.

    Returns:
        list: The updated intent_ranking list with modified confidence scores.

    """
    logging.debug("intent list")
    logging.debug(intent_ranking)
    logging.debug("end of intent list")

    # Initialize main and secondary associations
    main_associations = {}
    secondary_associations = {}

    # Load the YAML file
    with open('settings.yml', 'r') as file:
        settings = yaml.safe_load(file)

    # Retrieve the confidence_factors values
    confidence_factors = settings['confidence_factors']
    main_factor = confidence_factors['main_factor']
    secondary_factor = confidence_factors['secondary_factor']


    # Print the confidence_factors
    logging.debug(f"Main Factor: {main_factor}")
    logging.debug(f"Secondary Factor: {secondary_factor}")

    # Logging: Print positions of intent keywords
    logging.debug("Keyword positions")
    for intent in intent_ranking:
        intent_name = intent['name']
        keyword_regex = regex_patterns[f"{intent_name}_keywords"]
        matches = re.finditer(keyword_regex, user_input)
        for match in matches:
            keyword = match.group()
            position = match.start()
            logging.debug("Intent position")
            logging.debug(position)

            # Initial confidence score
            initial_score = intent['confidence']

            # Check if the intent is the highest confidence intent for the keyword
            if keyword not in main_associations or initial_score > main_associations[keyword]['confidence']:

                # Update main association for the keyword
                main_associations[keyword] = {
                    'intent': intent_name,
                    'confidence': initial_score,
                    'locations': [position]
                }
                logging.debug(f"Intent '{intent_name}': Keyword: Main Association, '{keyword}', Location: {position}, Initial Confidence: {initial_score}")
            elif initial_score == main_associations[keyword]['confidence']:
                if position not in main_associations[keyword]['locations']:

                    # Add the location to the main association for the keyword if the confidence score is the same. 
                    # This is to prevent secondary intents to not get increased too much by mutliple instances of the same keyword
                    
                    main_associations[keyword]['locations'].append(position)
                    logging.debug(f"Intent '{intent_name}': Keyword: additional detection, '{keyword}', Location: {position}, Initial Confidence: {initial_score}")
            else:

                # Add secondary association for the keyword
                if keyword not in secondary_associations:
                    secondary_associations[keyword] = []
                secondary_associations[keyword].append({
                    'intent': intent_name,
                    'confidence': initial_score,
                    'locations': [position]
                })

                logging.debug(f"Intent '{intent_name}': Keyword: Secondary Association, '{keyword}', Location: {position}, Initial Confidence: {initial_score}")
    logging.debug("end of keyword positions")

    # Update confidence scores for main associations
    for keyword, association in main_associations.items():
        association['confidence'] *= main_factor

        # Update intent confidence in intent_ranking for main associations
        for intent in intent_ranking:
            if intent['name'] == association['intent']:
                intent['confidence'] = association['confidence']
        
    # Update confidence scores for secondary associations
    for keyword, associations in secondary_associations.items():
        for association in associations:
            association['confidence'] *= secondary_factor

            # Update intent confidence in intent_ranking for secondary associations
            for intent in intent_ranking:
                if intent['name'] == association['intent']:
                    intent['confidence'] = association['confidence']

    # Print main associations
    logging.debug("Main Associations:")
    for keyword, association in main_associations.items():
        intent = association['intent']
        confidence = association['confidence']
        locations = association['locations']
        logging.debug(f"Intent '{intent}': Keyword: '{keyword}', Main Association, Locations: {locations}, Confidence: {confidence}")

    # Print secondary associations
    logging.debug("Secondary Associations:")
    for keyword, associations in secondary_associations.items():
        for association in associations:
            intent = association['intent']
            confidence = association['confidence']
            locations = association['locations']
            logging.debug(f"Intent '{intent}': Keyword: '{keyword}', Secondary Association, Locations: {locations}, Confidence: {confidence}")

    return intent_ranking


def intent_position(intent_name, user_input, regex_patterns):
    """
    Determines the position of the first occurrence of an intent's keyword in the user input.

    Args:
        intent_name (str): The name of the intent to match.
        user_input (str): The user input to search for keyword matches.
        regex_patterns (dict): The regex patterns used for intent matching.

    Returns:
        int: The position of the first occurrence of the intent's keyword, or sys.maxsize if not found.
    """

    # Load the YAML file
    with open('settings.yml', 'r') as file:
        settings = yaml.safe_load(file)

    # Retrieve the keyword_proximity value for detecting multiple intents
    keyword_proximity = settings['keyword_proximity']

    # Print the keyword_proximity
    logging.debug(f"Keyword Proximity: {keyword_proximity}")

    pattern = regex_patterns.get(intent_name, '')
    if pattern:
        matches = re.finditer(pattern, user_input, re.IGNORECASE)
        match_positions = [match.start() for match in matches]
        if match_positions:
            keyword_groups = []
            current_group = [match_positions[0]]
            for pos in match_positions[1:]:
                if pos - current_group[-1] <= keyword_proximity:  
                    current_group.append(pos)
                else:
                    keyword_groups.append(current_group)
                    current_group = [pos]
            keyword_groups.append(current_group)

            max_group = max(keyword_groups, key=len)
            return min(max_group)
    logging.debug(sys.maxsize)
    return sys.maxsize


def nonword_position(intent_name, user_input, regex_patterns, nonwords):
    """
    Determines the closest nonword to each of the respective intents.

    Args:
        intent_name (str): The name of the intent to match.
        user_input (str): The user input to search for keyword matches.
        nonwords (list): The list of nonwords associated with the intents.

    Returns:
        int: The position of the first occurrence of the intent's keyword, or sys.maxsize if not found.
    """

    logging.debug(f"Intent name: {intent_name}")
    logging.debug(f"User input: {user_input}")
    logging.debug(f"Regex patterns: {regex_patterns}")
    logging.debug(f"Nonwords: {nonwords}")

    pattern = regex_patterns.get(intent_name, '')
    if pattern:
        keywords = re.findall(r'\b\w+\b', pattern)
        logging.debug(f"Keywords: {keywords}")
        words = user_input.split()
        logging.debug(f"Words: {words}")
        intent_positions = [words.index(keyword) for keyword in keywords if keyword in words]
        logging.debug(f"Intent positions: {intent_positions}")
        nonword_positions = [index for index, word in enumerate(words) if word in nonwords]
        logging.debug(f"Nonword positions: {nonword_positions}")
        closest_distance = sys.maxsize
        closest_nonword = ''
        for intent_pos in intent_positions:
            for nonword_pos in nonword_positions:
                distance = abs(intent_pos - nonword_pos)
                logging.debug(f"Distance for intent position {intent_pos} and position {nonword_pos} : {distance}")
                if distance < closest_distance:
                    closest_distance = distance
                    closest_nonword = words[nonword_pos]
        logging.debug(f"Closest nonword: {closest_nonword}")
        return closest_nonword
    return ''

def process_intents(nlu_data, intents, entities, user_input, regex_patterns, output_widget, chat_prompt):
    """
    Processes the identified intents and performs corresponding actions based on the user input.

    Args:
        nlu_data (dict): The NLU data containing intent information.
        intents (list): The list of intents identified from the user input.
        entities (dict): The extracted entities from the user input.
        user_input (str): The user input text.
        regex_patterns (dict): The regex patterns used for intent matching.
        output_widget: The widget used for displaying output messages.
        chat_prompt: The ChatPrompt instance used for requesting additional input.

    Returns:
        None
    """

    entities_text = {}
    shared_data = []
    intents_with_positions = []

    logging.debug("Actions:")
    logging.debug(actions)


    if 'DEBUG_MODE' in actions:
        DEBUG_MODE = True
    else:
        DEBUG_MODE = False

    for intent in intents:
        intent_name = intent["name"]
        action_key = actions.get(intent_name)

        logging.debug(f"Current intent: {intent_name}, action key: {action_key}")

        if action_key:
            # Extract keywords for the intent
            pattern = regex_patterns.get(f"{intent_name}_keywords", '')
            if pattern:
                matches = re.finditer(pattern, user_input, re.IGNORECASE)
                positions = [match.start() for match in matches]
            else:
                positions = []

            # Add the intent, action_key, and positions to the list
            intents_with_positions.append((intent, action_key, positions))

    # Sort intents based on the positions of their first keyword occurrence
    intents_with_positions.sort(key=lambda x: x[2][0] if x[2] else sys.maxsize)

    entities_by_intent = {}
    for item in nlu_data["nlu"]:
        if "intent" in item:
            intent_name = item["intent"]
            entities_to_include = []
            examples = item["examples"].split('\n')
            for example in examples:
                assoicated_intent = re.findall(r"\((.*?)\)", example)
                for entity in assoicated_intent:
                    if entity not in entities_to_include:
                        entities_to_include.append(entity)
            logging.debug(f"'{intent_name}' has the following entities: {', '.join(entities_to_include)}")
            entities_by_intent.setdefault(intent_name, []).extend(entities_to_include)
                
    logging.debug("end of entities by intent")
    logging.debug(entities_by_intent)


    if entities:
        entities_text = {key: value for key, value in entities.items()}

        logging.debug(entities_text)


    # stores a list of all nonwords from the users_input this is used to assist with entity detection for things software or company names
    nonwords = find_nonwords(user_input)
    logging.debug("Nonwords found:")
    logging.debug(nonwords)

    logging.debug("entities list")
    logging.debug(entities_by_intent)
    logging.debug("End of entities list.")

    # This is assign nonwords to entities that have the flag for dynamic nonword usage. IE software or company names.
    for entity in nlu_data["nlu"]:
        if "regex" in entity:
            entity_label = entity["regex"]
            logging.debug("Entity label")
            logging.debug(entity_label)
            examples = entity["examples"].split('\n')
            for example in examples:
                logging.debug("Entity keywords")
                logging.debug(example)                
                example = example.split("|")
                example[0] = example[0].lstrip("- ")
                logging.debug(example)
                if any(flag == "nonwords_flag" for flag in example):
                    for intent, entity_list in entities_by_intent.items():
                        if entity_label in entity_list:
                            if entity_list[0] in entities_text:
                                logging.debug("Entity List")
                                logging.debug(entity_list)
                                entity_value = entity_list[0]
                            else:
                                if nonwords:
                                    # needs to do both because one is for display and one is for actions
                                    logging.debug('Else entity list')
                                    current_intent = next((intent for intent, entities in entities_by_intent.items() if entity_list[0] in entities), None)
                                    current_intent = current_intent + "_keywords"
                                    logging.debug(entity_list[0])
                                    logging.debug(current_intent)
                                    nonwords_string = '|'.join([str(item) for item in nonwords])
                                    closest_nonword = nonword_position(current_intent, user_input, regex_patterns, nonwords)
                                    entities_text[entity_list[0]] = closest_nonword
                                    entities[entity_list[0]] = closest_nonword
                                    logging.debug("closest nonword")
                                    logging.debug(closest_nonword)
            logging.debug("Entities by intent")
            logging.debug(entities_by_intent)

    logging.debug("Nonwords found:")
    logging.debug(nonwords)
    logging.debug("End of found nonwords")
    logging.debug(entities_by_intent)
    logging.debug(entities_text)

    pending_actions = []

    if DEBUG_MODE == True:
        pending_actions.append("DEBUG_MODE")
    else:
        for intent in intents:
            action_key = intent["name"]
            if action_key:
                for key, value in entities.items():
                    action_key = action_key.replace("{" + key + "}", value)
                pending_actions.append(action_key)
                logging.debug(f"Actions: {pending_actions}")

    # For multiple actions
    if len(pending_actions) > 1:
        actions_text = ", ".join(pending_actions[:-1]) + " and " + pending_actions[-1]

        action_confirmations = []
        for action_key in pending_actions:
            confirmation_msg = f"AI: I detected the action: {action_key}"
            if action_key in entities_by_intent:
                entity_info = []
                for entity in entities_by_intent[action_key]:
                    if entity in entities_text:
                        entity_info.append(f"{entity}: {entities_text[entity]}")
                entity_info_text = ', '.join(entity_info)
                confirmation_msg += f" with entities: {entity_info_text}"

            action_confirmations.append(confirmation_msg)
        actions_text = "\n".join(action_confirmations)
        output_widget.append(f"AI: Detected multiple actions:\n{actions_text} Do you want to proceed with these actions? (yes/no)")

        while True:
            chat_prompt.expecting_additional_info = True
            chat_prompt.request_input("Please type 'yes' or 'no':")
            user_input = chat_prompt.wait_for_input().strip().lower()
            if user_input == "yes":
                for action_key in pending_actions:
                    logging.debug("shared data:")
                    logging.debug(shared_data)
                    working_action = [action_key, actions.get(action_key, {}).replace("action_", "", 1)]
                    execute_action(working_action, entities, shared_data, output_widget, chat_prompt)
                break
            elif user_input == "no":
                output_widget.append("AI: Okay, no actions will be executed.")
                break
            else:
                output_widget.append("AI: Invalid input. Please type 'yes' or 'no':")

    # For single action
    elif len(pending_actions) == 1:
        action_key = pending_actions[0]

        if action_key in entities_by_intent:
            entity_info = []
            for entity in entities_by_intent[action_key]:
                if entity in entities_text:
                    entity_info.append(f"{entity}: {entities_text[entity]}")
            entity_info_text = ', '.join(entity_info)
            output_widget.append(f"AI: I detected the action: {action_key} with entities: {entity_info_text}. Do you want to proceed with this action? (yes/no)")
            
        else:
            output_widget.append(f"AI: I detected the action: {action_key}. Do you want to proceed with this action? (yes/no)")
    
        while True:
            chat_prompt.expecting_additional_info = True
            chat_prompt.request_input("Please type 'yes' or 'no':")
            user_input = chat_prompt.wait_for_input().strip().lower()
            if user_input == "yes":
                logging.debug("list of actions")
                logging.debug(actions)
                logging.debug("end of list")
                working_action = [action_key, actions.get(action_key, {}).replace("action_", "", 1)]
                execute_action(working_action, entities, shared_data, output_widget, chat_prompt)
                break
            elif user_input == "no":
                output_widget.append("AI: Okay, no action will be executed.")
                break
            else:
                output_widget.append("AI: Invalid input. Please type 'yes' or 'no':")
    else:
        output_widget.append("AI: I'm not sure what you want to do.")

    # Print the extracted keywords for each intent
    for intent, action_key, positions in intents_with_positions:
        intent_name = intent["name"]
        pattern = regex_patterns.get(f"{intent_name}_keywords", '')
        if pattern:
            matches = re.findall(pattern, user_input, re.IGNORECASE)
            keywords = ', '.join(matches)
        else:
            keywords = ''
        logging.debug(f"Intent '{intent_name}' keywords: {keywords}")
        
def prepare_intent_patterns(training_data):
    """
    Generates regex patterns for intent matching based on the training data.

    Args:
        training_data (dict): The training data containing examples and regex patterns.

    Returns:
        dict: The generated regex patterns for intent matching.
    """
    regex_patterns = {}
    for item in training_data['nlu']:
        if item.get('regex'):
            regex_name = item['regex']
            regex_pattern = r'\b(?:' + '|'.join([re.sub(r'\|(?!\))', '|', keyword) for keyword in item['examples'].splitlines()]) + r')\b'
            regex_pattern = regex_pattern.replace(r'\b(?:- ', r'\b(?:- |')
            regex_patterns[regex_name] = regex_pattern
    logging.debug("Generated regex patterns:", regex_patterns)
    return regex_patterns


def detect_keyword_positions(text, regex_patterns):
    """
    Detects the positions of keywords in the text based on the provided regex patterns.

    Args:
        text (str): The text to search for keyword positions.
        regex_patterns (dict): The regex patterns for keyword matching.

    Returns:
        dict: The detected keyword positions, where keys are intent names and values are lists of positions.
    """
    keyword_positions = {}
    for intent_name, pattern in regex_patterns.items():
        regex = re.compile(pattern, re.IGNORECASE)
        matches = list(regex.finditer(text))
        if matches:
            keyword_positions[intent_name] = [match.start() for match in matches]
    return keyword_positions

def extract_keywords(text, intent_patterns):
    """
    Extracts keywords from the text based on the provided intent patterns.

    Args:
        text (str): The text to extract keywords from.
        intent_patterns (dict): The intent patterns for keyword extraction.

    Returns:
        dict: The extracted keywords, where keys are intents and values are lists of extracted keyword matches.
    """
    keywords = {}
    for intent, pattern in intent_patterns.items():
        regex = re.compile(pattern, re.IGNORECASE)
        matches = regex.findall(text)
        logging.debug(f"Intent: {intent}, Pattern: {pattern}, Matches: {matches}")
        if matches:
            keywords[intent] = matches
    return keywords

# Function to count the number of words in a text
def word_count(text):
    return len(text.split())
