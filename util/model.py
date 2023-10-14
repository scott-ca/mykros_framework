import asyncio
from rasa.shared.nlu.training_data.message import Message
from rasa.core.agent import Agent
import logging

# Import translate_message from translator.py
from util.translator import translate_message

class Model:
    """
    A class for loading the rasa NLU model.

    Args:
        model_path (str): The path to the NLU model. This is used in the rasa_model module.

    Attributes:
        agent (Agent): The loaded NLU agent.

    Methods:
        message: Process a user message and return the parsed result.
    """
        
    def __init__(self, model_path: str) -> None:    
        self.agent = Agent.load(model_path)
        print("NLU model loaded")

    def message(self, message: str) -> Message:
        """
        Process a user message and return the parsed result.

        Args:
            message (str): The user message to be processed.

        Returns:
            Message: The parsed result of the user message.
        """

        if message.lower() not in ["yes", "no"]:
            # Translate the message if needed
            logging.debug(f"pre:translation {message}")
            message = translate_message(message)
            logging.debug(message)
            logging.debug(f"post translation: {message}")

        # Replace symbols with their respective placeholders
        message = message.replace('/', '__FSLASH__')
        message = message.replace('%', '__PERCENT__')
        message = message.replace('\\', '__BSLASH__')
        message = message.replace('-', '__DASH__')
        message = message.strip()
        result = asyncio.run(self.agent.parse_message(message))
        return result
