from PySide2.QtWidgets import QApplication, QWidget
from spellchecker import SpellChecker

from util.rasa_model import rasa_model


def request_additional_info(chat_prompt, prompt_text=None):
    """
    Requests additional information from the user based on the expected intent.

    Args:
        chat_prompt (ChatPrompt): The ChatPrompt instance used for requesting additional input.
        info_type (str): The type of information expected (e.g., 'file_name', 'url', 'timer').
        prompt_text (str, optional): The prompt text to display for the additional input. Defaults to None.
        allow_any (str, optional): This allows the entity to be assigned any value. Defaults to False

    Returns:
        str: The additional information provided by the user.
    """
    # Define the mapping of expected intents that may requiere additional information


    # Loops prompting for missing entity input until valid input is provided.
    while True:
        chat_prompt.expecting_additional_info = True
        chat_prompt.request_input(prompt_text + "\nYou may type /cancel to cancel this operation")
        user_input = chat_prompt.wait_for_input().strip()
        

        # Check if the user input is "/cancel"
        if user_input.lower() == "/cancel":
            return None

        else:
            response = rasa_model.message(user_input)
            intent = response["intent"]["name"]
            
            return user_input

def intent_help(message, intent_info, output_widget):
    """
    Provides both a summary of each of the intents as well as a more details information for specific intents. 

    Args:
        message : The message the user entered into the chat prompt.
        output_widget (QTextEdit): The QTextEdit widget used for displaying output.

    Returns:
        str: The additional information provided by the user.
    """
    

    intent_name = message[6:].strip()
    
    if intent_name == "general" or intent_name in intent_info:
        if intent_name == "general":
            output_widget.append('You can speak conversationally with the AI to complete various tasks.'
            'For example you could type "Can you open my firefox bookmark banking" and it will launch your browser to the url in that bookmark.'
            'For more information on a specific intent type /help followed by the intent name IE. /help list do_math'
            'Please see the list of avalible intents and a brief description of what they do.\n')
        
            # Display detailed summaries for each intent
            for intent, summary in intent_info.items():                
                output_widget.append(f"{intent}: {intent_info[intent]['summary']}")
        else:
            # Display detailed summary for selected intent
            output_widget.append(f"{intent_name}: {intent_info[intent_name]['details']}")

    else:
        output_widget.append(f"AI: Unknown intent. Please type /help for more information.")
    
def find_nonwords(user_input):
    spell = SpellChecker()
    words = user_input.split()
    nonwords = []
    for word in words:
        # Skip the word "spellchecker" or "spellcheck"
        if word.lower() == "spellchecker" or word.lower() == "spellcheck":
            continue
        if not spell.correction(word) == word:
            nonwords.append(word)
    return nonwords