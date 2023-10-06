import os
import logging
import platform
import importlib
import inspect
import sys

def execute_action(working_action, entities, shared_data, output_widget=None, chat_prompt=None):
    """
    Executes the specified action based on the provided action string and entities.

    Args:
        action (str): The action string to execute.
        entities (dict): The entities extracted from the user input.
        output_widget (QTextEdit, optional): The QTextEdit widget used for displaying output. Defaults to None.
        chat_prompt (ChatPrompt, optional): The ChatPrompt instance used for interacting with the user. Defaults to None.
    """
    os_name = platform.system()
    logging.debug(f"action_parts: intent,action received: {working_action}")
    logging.debug(f"action_parts: {working_action}")
    # Set to true for testing new action_parts. When set true will only run that action and no others.


    # Construct the action module name with subfolder check
    action_module_name = f"custom_actions.{working_action[1]}.{working_action[1]}_executor"

    # Check for subfolders in custom_actions
    subfolder_names = ["file_actions", "system_actions", "misc_actions", "web_actions", "word_actions", "debug_actions" ]
    for subfolder_name in subfolder_names:
        subfolder_check = f"custom_actions.{subfolder_name}.{working_action[1]}.{working_action[1]}_executor"
        try:
            print(subfolder_check)
            action_module = importlib.import_module(subfolder_check)
            subfolder_module_name = f"custom_actions.{subfolder_name}.{working_action[1]}.{working_action[1]}_executor"
            print("module found")
            break
        except ModuleNotFoundError:
            pass
        

    # Dynamically load the action executor module based on the action_module_name
    action_module = importlib.import_module(subfolder_module_name)

    # Get the custom action function from the loaded module
    action_function_name = f"{working_action[1]}_execution"
    action_function = getattr(action_module, action_function_name)

    # Get the parameters of the custom action function
    action_signature = inspect.signature(action_function)
    action_args = []

    for param_name, param in action_signature.parameters.items():
        if param_name == 'output_widget':
            action_args.append(output_widget)
        elif param_name == 'entities':
            action_args.append(entities)
        elif param_name == 'shared_data':
            action_args.append(shared_data)
        elif param_name == 'chat_prompt':
            action_args.append(chat_prompt)
        elif param_name == 'os_name':
            action_args.append(os_name)
        elif param_name == 'working_action':
            action_args.append(working_action[0])

    # Execute the action function with the prepared arguments
    action_function(*action_args)