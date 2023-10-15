# Mykros framework

&nbsp;
&nbsp;

# Table of contents
* [Summary](#summary)
* [Why choose the Mykros framework](#why-choose-the-mykros-framework)
* [Roadmap](#roadmap)
* [Installation instructions](#installation-instructions)
* [Running Mykros](#running-mykros)
* [Adding custom actions](#adding-custom-actions)
* [License](#license)

## Summary

Mykros is an open sourced portable AI assistant framework, offering compatibility with both Windows and Linux and can even be run directly from a USB drive. Designed to streamline your daily workflow using natural language, and improving efficiency and productivity with your day-to-day tasks.

The Mykros framework also provides the flexibility to interact with models using your native language even if the model was trained on data in another language. You are also able interact with custom actions that were created in another languages. 

The Mykros framework utilizes the Rasa model for intent and entity detection while internalizing dialog and action management. By managing conversations and actions internally, Mykros eliminates the need for an external action server. This allows Mykros to reduce complexity, add functionality, increase flexibility and performance, and increase accuracy while only needing small amounts of training data.

By combining the strengths of the Mykros framework and the lightweight Rasa model, Mykros delivers a powerful and modular user friendly AI assistant solution.

&nbsp;
&nbsp;

## Why choose the Mykros framework 

The Mykros framework was design with a few key principles in mind.

### Privacy
While everyone has different privacy requirements, it is important to know what happens to your data and to have the choice of what happens to the data. Mykros is designed to run locally, ensuring you retain full control over your data. This ensures a greater level of privacy compared to cloud-based alternatives as everything is stored and run locally.

### Lightweight and efficient resource usage
New technology and tools should be accessible to everyone. While typically most advancements will require newer hardware, that doesn't mean we shouldn't strive for technology and tools that don't require cutting edge hardware. 

Mykros is optimized for resource efficiency, requiring approximately 1GB of RAM and 3.5GB of diskspace. The model is also lightweight; even with 30 intents and their respective training data, the model size remains under 40 MB. The model has been designed to run efficiently even on devices without a dedicated GPU, making it a good option even for lower-end hardware configurations and running along side other applications that may otherwise require those resources. Mykros has been tested on high end hardware, low end virtual machines, and low end hardware while retaining the same functionality. 

Mykros can also be run from a USB drive allowing you to use it between multiple devices and operating systmes with ease.

### Modularity and expandability
Designed with modularity at its core, Mykros offers an adaptable framework that caters to individual needs and workflows. While its foundation is python based, its flexible design integrates seamlessly with existing code, even those from non-native frameworks or even other programming languages, provided they interface through the Mykros python entry point for the custom action.

You can create custom actions tailored to your needs, whether it's custom action to simplify interactions with a third-party tool you frequently use, streamline intricate computer tasks, set a timer using natural language, or even locate the latest cat videos. The possibilities are extensive. Moreover, you have the flexibility to deactivate any action, built-in or custom, and without needing to delete the actual action.

Mykros has been designed to be as modular as possible even outside of the custom actions, allowing you to customize various components to suit your specific needs. For instance, the translation feature in Mykros is compartmentalized, making it straightforward to replace with a different library or tool if should you prefer to use something else to handle that component. This modularity ensures that you can adapt and customize Mykros to meet your specific needs while maintaining the overall functionality of the AI assistant.

### Accessibility
Accessibility encompasses numerous facets, with language accessibility often being an overlooked. Often leaving groups who may find interaction with these models prohibitive due to the languages the models were originally trained on, which may not include their native language. While the rationale behind this is sound, the result is the same leaving groups of people unable to use the technology.

Mykros addresses this issue by not only allowing the use of these models in your preferred language but also by allowing the flexibility of interacting with custom actions in that language as well. This also allows for the option of translating only the input for intent detection, all input, all output, or both input and output.

Given the ease of adding custom actions, should you have standalone code that is not in your preferred language and as a result causing it to be difficult navigate and use, you can add it as a custom action and then interact with it in your language of choice through the assistant.

This is all done offline to maintain privacy and also allowing allowing the flexibility to be used on devices without an internet connection.

### Advanced intent management and workflow automation
With Mykros you can execute single actions, independent multiple actions, or link them together to create powerful workflows. Linking actions allows the output of one action to act as the input for another action, enabling sophisticated chaining and automation. Additionally, the intent detection and entity extraction has been improved, and without needing large amounts of training data. Typically only needing around 20 examples for each new action. A simple action may require as little as 5 examples and complex actions that extracts multiple pieces of data may only require 50 or less examples of how the action may be requested.

**Additional information**

You can an see some examples of custom actions that could be created in a project that uses the framework called Mykros Assist. The list of that projects built-in custom actions along with their descriptions can be found inside of the intent_config.yml file found [here](https://github.com/scott-ca/mykros_assist/blob/main/intent_config.yml)

&nbsp;
&nbsp;

## Roadmap

Mykros is more than merely another AI framework. It's also about ensuring the advancements in AI remains accessible to as broad of range of people as possible. In an industry that is rapidly evolving, it also means evolving Mykros as well.

Everyone has unique technology requirements and preferences when it comes to the tools they use, as well as limitations that determine which tools they cannot or choose not to use. While we can't reach everyone or meet every requirement, that doesn't mean we shouldn't strive to.

Privacy, for some, is paramount, requiring a greater need for control over their own data. For others, their limitations resides in access to hardware, whether it be high-end hardware or simply adequate storage capacity. While others, on the other hand, may be limited by the lack of stable internet access or may not have access to the internet at all. Some even may have all the access, but simple do not speak the native language the tools were developed in and as a result cannot use the tool.

Sometimes, it's as simple as having the choice and the flexibility to access tools that work best for you, in the way that works best for you.

Advancements often increase accessibility, but they can also sometimes widen existing limitations or even introduce new ones.

These requirements and restrictions are constantly changing and evolving. Mykros strives to keep pace with these developments.


Below are areas of potential development, which can explore either directly or collaboratively with the community.

- **Auto detect input language**: Explore the potential feature and overhead that would be added by having an option to set the input language to "auto-detect". If implemented, it would be optional and always have the option to specify the language or disable translation completely, bypassing any overhead used by this functionality.

- **Updates**: Introducing an option to update to allow for updating the version of the framework and/or AI assistant. This would involve a manual check for updates to ensure it isn't accessing the internet without your knowledge and causing software instability by the updates. It would be customizable so that developers can update the framework while also giving users of various AI assistant built on the framework the option to update to the latest version of the assistant. The latter option would allow users to update the specific AI assistant and not necessarily the framework itself and as such would allow the option to point to where the developer stores their update files.

- **Backup and restore**: : Incorporating the ability to create environment backups during direct changes made by the developer utilizing the framework or automatic backups during updates. The system would retain a set number of backups, facilitating easy restoration to a previous version in cases of incompatibility or other issues.

- **Offline voice integration**: Exploring options for offline voice integration, potentially with a distinct keybinding to ensure intentional activation when enabling the feature.


Your feedback and contributions toward these future developments are greatly welcomed and appreciated!

## Installation instructions

Mykros has been tested across a range of systems including lower-end hardware, medium to higher-end hardware, as well as virtual machines running both Windows and Linux. While the Linux testing has been concentrated on Debian/Ubuntu-based distributions, it should function on other distributions as long as libxcb-xinerama has been installed on the respective distribution. The lower end hardware that was used for testing was a 10 year old laptop.


The time required for setting up Mykros can vary based on your hardware specifications and internet connection speed. Please note, while the setting up of the environment may take a decent bit longer on a lower end computer, the usage of Mykros once the setup is complete will remaining quick and responsible even on lower-end hardware.


### Setting up the environment - Estimated time

- **Lower-end hardware:** On older hardware with a slower internet connection, the initial setup may take 5 to 15 minutes. This includes downloading the Miniconda portable installer and required Python libraries.

- **Medium to higher-end hardware:** On medium to higher end hardware, the setup process takes approximately 2 minutes.

### Model Training - Estimated time

After setting up the environment, you'll need to train the model. This is a one-time process, unless you plan to incorporate additional training data or custom actions later on. The training process is CPU-based and does not utilize the GPU. Therefore, having a dedicated GPU won't have an impact on this process.

- **Lower-end hardware:** On older hardware, model training may approximately 15 minutes. 
- **Medium to higher-end hardware:** On medium to higher end hardware the model training process can be completed in about 2 minutes.


## Instructions

*Note: If you wish to run this from a USB drive, while you can do the setup directly on the USB drive it is recommended to do it on your local hard drive and manually copy the files over to reduce environment configuration time. You can then launch the files directly from the USB drive since it is local to the folder and not your computer.*

### Step 1: Clone the Mykros framework repository

If you have Git installed, open a terminal or command prompt and execute the following command to clone the repository:
```
git clone https://github.com/scott-ca/mykros-framework.git
cd mykros_framework
```
Alternatively, you can manually download the files by clicking the "Code" button at the top right of the webpage and selecting "Download ZIP." Extract the downloaded ZIP file to your chosen directory. Open the command prompt or terminal in the extracted folder.


### Step 2: Setting up the environment


Mykros is designed to be portable, utilizing a portable version of Miniconda to create an isolated environment named portable_env. This approach eliminates the need for a prior python or conda installations, and as such won't interfere with any existing installations you may have.

### Prerequisites

If you are on windows, there are no prerequisites.

If you are on linux, and using X11 you will need to install libxcb-xinerama package, which is required by PySide to manage the GUI interface. This package does need to be locally installed as it is unable to be loaded from the portable environment, and as a result needs to be installed even in the case where you run this from a usb drive.

**Debian/Ubuntu:** 
```
sudo apt-get install libxcb-xinerama0
```
**Fedora:** 
```
sudo dnf install libxcb-xinerama
```
**CentOS/RHEL:**
```
sudo yum install libxcb-xinerama
```
**Arch:**
```
sudo pacman -S libxcb
```
**Gentoo:**
```
sudo emerge libxcb
```


### Downloading and configuration of the portable the environment(recommended)

To download the portable Miniconda installer and configure the environment as well as generate the model from the training data you will need to run the following command in your command prompt/terminal.

**On Linux**
```
./update_data.sh
```
**On Windows**
```
update_data.bat
```
### Alternative configuration

Alternatively, if you wish to use your own previously installed conda environment or non-conda python environments, you can run update_data.py directly instead of using the provided scripts, as they launch the script with the assumption of using the portable environment.

If you are using your own installation of Conda/Miniconda
```
create -y mykros_framework python=3.10.4
pip install -r requirements.txt
python update_data.py
```

## Running Mykros

This repo is for the framework, and while you can run the framework with the included example data the usage is better illustrated with additional training data and custom actions included. 

Thus for reference I have provided usage documentation below from Mykros assist repo found [here](https://github.com/scott-ca/mykros_assist) that has training data and custom actions already added. 

The custom actions that are included in the framework are example_mute_computer and example_open_app. These actions will show their respective test messages and no changes would be made on your computer.

The below reference documentation however will reference the custom actions from the other project to better illustrate the features of the framework.

### Running Mykros using the portable environment (recommended)


You have two methods of running Mykros, silently and verbosely. 

To run it silently run the command below in the command prompt/terminal

**On Linux**
```
./run_linux.sh
```
**On Windows**
```
run_windows.vbs
```

To run it verbosely so that you will see the environment setup as well as any processing that happens as you use Mykros use the command below in the command prompt/terminal

**On Linux**
```
./verbose_linux.sh
```
**On Windows**
```
verbose_windows.bat
```

Mykros will take a minute or two to launch the script and load the model into memory. Once it has been loaded you will see the black book icon in your system tray, usually near the clock in the top right or bottom right corner of the screen.

![icon](https://github.com/scott-ca/mykros_assist/assets/59944183/b73fe786-9005-43bd-9cc3-9899a67d9365)


Once it has been loaded and you see the icon then you can open the assistant by using the keyboard shortcut of ctrl + `(backtick) located on the top left of your keyboard. This will open a chat window as shown below.

<img src="https://github.com/scott-ca/mykros_assist/assets/59944183/32aea4b4-cb11-4f22-b7f6-6077d1805bef" width="300" height="217">

### Alternative launching of Mykros

Alternatively, if you wish to use your own previously installed conda environment or non-conda python environments, you can run mykros_framework.py directly instead of using the provided scripts, as they launch the script with the assumption of using the portable environment.

If you are using your own installation of Conda/Miniconda
```
python mykros_framework.py
```
&nbsp;
&nbsp;

## Usage

Mykros offers three distinct ways of processing actions. Any actions over the confidence threshold and their respective associated extracted data, which is also known as entities will be displayed.

You will also need to confirm any action before it is processed. Should any additional entity information be required that wasn't extracted it will ask for it at this time. A full list of all of the built-in actions along with their descriptions inside of the intent_config.yml file found [here](https://github.com/scott-ca/mykros_assist/blob/main/intent_config.yml)

### Processing single actions

Below is an example of processing a single action and what it would look like.

IE. If you type in "Can you search for a file containing the text sales in /home/test/Desktop" you will get an output similar to what is shown below.
```
You: Can you search for a file containing the text sales in /home/test/Desktop
AI: I detected the action: search_file_content with entities: file_query: sales, folder_query: /home/test/Desktop. Do you want to proceed with this action? (yes/no)
AI: Please type 'yes' or 'no':
```
Once you confirm the action it will process the detected intent using the extracted entities. In this case "show any files in the folder /home/test/Desktop that contain the word sales within the file contents".

### Processing multiple actions
Below is an example of processing multiple actions and what it would look like. 

IE. If you type in "Can you list the files in /home/test and open the terminal" you will get an output similar to what is shown below. 
 ```
AI: Detected multiple actions:
AI: I detected the action: list_files with entities: folder_query: /home/test
AI: I detected the action: open_terminal with entities: Do you want to proceed with these actions? (yes/no)
AI: Please type 'yes' or 'no
```
Once you confirm the action it will process the detected intents using the extracted entities in the order they were detected.

### Processing linked actions
Linked actions are similar to multiple actions with an additional functionality. They allow the output of one action to be used as input for another action. This is made possible through the specific import/exported entities linked to each intent. This functionality needs to be specifically configured for intents that wish to allow for the functionality. If it isn't supported by the action it will prompt for any missing information. This is triggered by the usage of export/exported and import/imported.

IE. If you type in "Can you export the list of files in /home/test/ and import the data to a new file in /home/test/test_file.txt and export that file and open the imported file" you will get an output similar to what is shown the below. 
```
AI: Detected multiple actions:
AI: I detected the action: list_files with entities: folder_query: /home/test/, list_files_export: export
AI: I detected the action: create_file with entities: create_file_path: /home/test/test_file.txt, create_file_import: import, create_file_export: export
AI: I detected the action: open_file with entities: open_file_import: import Do you want to proceed with these actions? (yes/no)
AI: Please type 'yes' or 'no':
```

This will display the list of files in /home/test/ and create a file with that list in /home/test/test_file.txt and then open the file. This will also allow you to see which actions are importing and which actions are exporting data.

Furthermore, this usage can bypass conflict groups depending on the frequency of 'export/exported' in the user input. 


Conflict groups exist to prevent the detection of multiple intents when only a single intent should be detected. They increase accuracy when detecting multiple intents. For example, if a user types "Can you create me a list of the files in the directory /home/test/", without a conflict group, Mykros might misinterpret the intent and attempt to create a file and list the files simultaneously. However, if the user types "Can you export a list of the files in the directory /home/test/ and import them into /home/test/test_folder/test_file/", Mykros allows for both actions to be detected since the user is intentionally linking the two intents via the export/exporting keywords.

&nbsp;
&nbsp;

### Additional Configuration and Customization

### <ins>Basic</ins>

**Auto-start:** If you would like to have Mykros start automatically with your computer you can the commands below in your command prompt/terminal

On Linux
```
./linux_startup.sh
```
On Windows
```
windows_startup.bat
```
&nbsp;

In Windows this will add Mykros to your startup folder and in linux to your ~/.config/autorun/ folder allowing it to boot up automatically when you start your computer.

**Built-in help:** If you require information on any of the intents, you can use the built-in help function. Typing /help will list all the intents along with a brief summary of each intent. If you need more detailed information on a specific intent, type /help followed by the name of the intent. For example, /help mute_computer. This information can also be referenced in the intent_config.yml file.

### <ins>Advanced</ins>

**Disabling actions:** The intent_config.yml file in the main folder allows you to disable any intents or actions. If you disable any, you will need to run update_data.py from the terminal or command prompt via "python update_data.py". This script updates the training data based on your changes in intent_config.yml.

Please note, you need to have at least 2 intents/actions enabled in the intent_config.yml to allow for proper detection of the intents. Otherwise you will get an nlu_fallback error.

**Resolving intent conflicts:** If you encounter overlapping intent detections, you can modify the conflict_groups.yml file in the main directory. A conflict group is a set of intents that can't be executed simultaneously. Only the intent with the highest confidence score will be executed. The groups however are bypassed when using linked actions.

Below is an example of some conflict groups:

```
conflict_groups:
  - name: App actions
    intents:
      - open_app
      - close_app
  - name: Mute computer actions
    intents:
      - mute_computer
      - unmute_computer
```

**Modifying detection settings**
If you wish to modify any detection settings, you can do so via the settings.yml file located in the main directory. There are 3 settings included in the config file confidence threshold, keyword_proximity, confidence factors. These files don't need to be updated in order to add your own custom actions.


**confidence_threshold** - This is the threshold for the required confidence score for an intent to be detected. This is a global score for all intents. If the score is too high then you risk your actions not being detected, if the score is too low you risk multiple actions being detected when only a single action is intended.

**keyword_proximity** - This is used for detecting multiple intents. This is the proximity the keywords need to be to be considered part of the same intent vs a secondary intent. 

**confidence_factors** - By default the Rasa model assigns a significantly lower confidence scores to secondary intents. This in turn significantly decreases the likelihood of multiple intents being detected accidentally, unfortunately it also reduces the likelihood of multiple intents being detected intentionally.

If you choose to lower the confidence score to compensate you tend to accidentally detect multiple intents, not only in instances where you only intend for a single intent but also potentially detecting three intents when you only have two.

This occurs because of the large difference between the confidence scores of the main intent and any additional intent, while the disparity between additional intents remains quite small. 

The confidence_factors are used to increase the confidence scores of intents based on the surrounding keywords for the respective intents. This has two main purposes. 

The first purpose is to increase the disparity between all of the secondary intents, as well as help bring them closer to the confidence threshold. The second purpose is that if all of the intents are under the threshold it will help bring the main intent over the threshold via matching with detected keywords and thus increasing the detection of the correct intent.

The confidence factors uses two variables main_factor and secondary_factor The main factor is the intent with the highest confidence score that has that keyword and secondary factor is any intent excluding the highest confidence score. I have included a snippet of what it looks like in the settings file.

```
confidence_factors:
  main_factor: 30
  secondary_factor: 10
```
We will use the command "Can you list the files in /home/test and open the terminal" to illustrate what this looks like. This example is intentionally triggering multiple intents, the same however is also true even with a single intent.


Without the added functionality we get confidence scores below. 

```
list_files has a confidence of 0.8917641043663025
run_terminal has a confidence of 0.05301111564040184
open_terminal has a confidence of 0.018960289657115936
antonymize_word has a confidence of 0.006223676260560751
```

While list_files is well above the default confidence_score threshold of 0.2. The next 3 intents are significantly lower than the initial intent. The disparity makes it difficult to accurately detect multiple intents without creating false positives. In addition, this is compounded when you have additional intents as the disparity between intents will become even smaller.

While it will be uncommon to use more than two independent intents simultaneously, that will change if you choose to link them together as that allows you to use the outputs from one action as inputs for other. 


Using the same example as before with using the functionality the intents confidence scores has changed as shown below.

```
list_files has a confidence of 26.752923130989075
open_terminal has a confidence of 0.5688086897134781
run_terminal has a confidence of 0.05301111564040184
open_file_explorer has a confidence: 0.02363760955631733
open_browser has a confidence of 0.017924007261171937
antonymize_word has a confidence score of 0.006223676260560751
```

This has increased the accuracy of the intents including ones previously under the threshold as well as increasing the disparity between between the secondary intents. As a result open_terminal now has a higher confidence score than run_terminal which is the correct intent that should be detected. In addition, previously the fourth highest intent was antonymize_word where as now both open_file_explorer and open_browser are significantly higher, which would be a lot more accurate than antonymize_word. 

**translation:** This setting is used to enable you to interact with models and custom actions that are not in your preferred language. There are six values shown below. They are enable, input_intent_detection, all_input, all_output, from_language, to_language.

translation:
    enable: true
    input_intent_detection: true
    all_input: true
    all_output: true
    from_language: sk
    to_language: en


The enable value is for the translation function as a whole. If this is set to any value other than true, no translation will occur.

The input_intent_detection value controls whether translation functionality applies to text you input for intent and entity detection. 

The all_input value will apply the translation to your input for intent and entity detection the same as input_intent_detection, as well as extends the functionality to custom actions. When extended to custom actions it will automatically integrate without the custom action needing to support the functionality. Additionally, when set to true and the to_language is set to English you will be able to use either language for the yes/no confirmation. If the to_language is something other than English then you will need to use English for the yes/no confirmation. In addition while the /help and the /cancel functionality will be translated, the specific input of "/help" and "/cancel" will only function in English.

In most cases, you would want all of your input translated to your preferred language. With that said, there are some use cases where you may not wish to have all of your input translated. 

If for example you wanted a list of files in the folder and it was extended to the custom actions, then when you input
'''
listar archivos en la carpeta /casa/etc/ 
'''

it would try to list the folders in /home/etc/ which may not exist on your system.

You can bypass the translation of any part of the text in your input by surrounding it in double quotes. Using the previous example you could write

'''
listar archivos en la carpeta "/casa/etc/"
'''

Which then would look for folders in /casa/etc/. It would also remove the quotes, so that it interacts with the model as if you didn't include them. It only uses the quotes to detect what text it should bypass translation on.

Alternativly, you could disable translation for input and have it only translate output text, or disable translation entirly.

The all_output value controls whether the output text is translated. It will translate any output text that is in the to_language to the from_language. It works in the reverse of the input translation so that you have the option of interacting in both directions with the model. This will translate all_output including but not limited to the output from the custom actions.

The from_language is the language is your preferred language that will entering as your input. This is also used as the target output language should you enable output translation.

The to_language is the language the model, training data, and custom actions are in. This is also used as the source language for output and should match the language the model and custom actions are in.

While the functionality is enabled in any capacity, depending on the language, you may be able to interact with the models and the custom actions in both your preferred language and the language they were created in simultaneously without changing any settings. The reason for this is because in most cases when it attempts to translate the word and no translation is found then it will fail, thus leaving the word as it was original inputted in and as a result already in the intended language. 

The list of supported languages are below as well as in the settings.yml file.

"Arabic": "ar", "Azerbaijani": "az", "Catalan": "ca", "Chinese": "zh", "Czech": "cs", "Danish": "da", "Dutch": "nl", "English": "en", # "Esperanto": "eo", "Finnish": "fi", "French": "fr", "German": "de", "Greek": "el", "Hebrew": "he", "Hindi": "hi", "Hungarian": "hu", "Indonesian": "id", "Irish": "ga", "Italian": "it", "Japanese": "ja", "Korean": "ko", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Russian": "ru", "Slovak": "sk", "Spanish": "es", "Swedish": "sv", "Turkish": "tr", "Ukrainian": "uk"

When translation functionality is enabled, it will download the model automatically when you input any text. The models are specific to that language combination, for example English to French, and are stored in the translation_models folder and approximately 100-200 MB. Internet connectivity is only required to download the model, and not used while utilizing the model.

In addition, it will automatically utilize an intermediate language if one is installed. For example, if you have the es->en and en->fr models downloaded then you are able to translate from es->fr as if you had that direct model installed. This allows for translating between a larger variety of languages at the cost of minimal loss of quality.

The files are be automatically downloaded from [argosopentech](https://www.argosopentech.com/argospm/index/). 

Please note, the automatic downloading of the models only works for the direct translations. If you are utilizing an intermediate language then you will need to have it previously installed , or manually trigger the downloading of the model by setting the target and source languages including the intermediate language and then start the assistant so that it downloads that model and then repeat the process for the other model. At which time you can then set the from_language and to_language accordingly and it will automatically use the intermediate language. This would only be a one time process, and only is needed if you don't wish to use a model for the translation directly as that would automatically download.

&nbsp;

Should you wish too add your custom actions that is supported as well.
&nbsp;

## Adding custom actions

Custom actions can be easily integrated into Mykros. This involves creating a custom function, adding a small subset of training data to trigger the action, and update 2 configuration files and then running update_data.py.

To create a custom action you need create an intent and an action. In most cases you would have a single intent and a single action. However, you aren't restricted to that if your requirements are different.

You can assign multiple intents to the same action if you wish. Alternatively, you can also have a single or multiple entities tied to a single intent. They can also be shared between intents, however it is generally recommended to have a unique entity for each intent that requires an entity to ensure it is extracted how you expect.

Here is a breakdown of the components involved in creating custom actions:


**Intent(required):** The intent represents the desired action the user wants to perform. For instance, intents could be "search_google", "open_app", or "translate_webpage". Each intent is associated with a specific functionality or behavior.

**Entity(optional):** An entity refers to specific data Mykros extracts from the user's input that is used when processing the action. For instance, in the intent "search_google", the entity could be the search query provided by the user. 

You can also have multiple entities that are used by a single intent. For example, the intent search_file_content has two entities file_query and folder_query so that it can extract the search term as well as the folder path to search for the term in. This is optional, and if you don't require any additional context from the user beyond triggering the action, you can omit entities from the function.

**Action(required):** An action represents a specific functionality or behavior associated with one or more intents. They define how Mykros processes an intent. Most of the time, each action is tied to a single intent. If the action is tied to multiple intents, the action name should be distinct from the intent names.

An example of an action being assigned to multiple intents would be with intents define_word, antonymize_word, synonymize_word, hyponymize_word, hypernymize_word, homophonize_word which all share the action word_operation.

This is done so they can utilize the same custom action and process action differently depending on the intent it was called from without needing to duplicate that function for each intent. 

&nbsp;
### <ins>Action function</ins>

To add a custom action, start by creating a new action function. This function is just like any other python function with the exception of how the user input and output is handled.


You can use the template function located in the template folder. The template includes all the basic functionality that you may need, including the optional functionality. As a result, you can omit anything not needed when utilizing the template.  I will highlight the important parts of the template below. 


### Function header

The layout and structure is similar to other python functions you may create. You can also include classes in your custom action as long as the entry point for your module matches the function header and parmaters below (custom_actions).

def template_execution(output_widget, entities, chat_prompt, shared_data, os_name, working_action):


### Variables

All of the variables shown in the function header are passed into the function are optional. You can omit any of the variables not needed. However, the order is important for any that you do need and should match the order in the template. 

Below is a breakdown what each parameter is used for.

**output_widget:** This is used if you need to display any output to the user. This would also be needed if you have any required entities that require prompting from the user should they not be included in the original user input. The output_widget also has an optional parameter called bypass_translation that when set to true, which will ensure that the output isn't translated by translation component should you need to make sure it isn't altered. This only impacts what is displayed to the user, not what is processed your custom action.

**entities:** The entities extracted from the user input.

**chat_prompt:** The ChatPrompt object used for interacting with the user. This is used for when you need to prompt for any required entities that may require prompting the user should they not be included in the original user input. This can also be used for any input required that may not be tied to an entity.

**shared_data:** Shared data for exporting and importing data between intents should your function support this functionality.

**os_name: os_name (str):** The name of the operating system.

**working_action (str):** The name of the intent that called the action.


### Requesting additional information

When extracting any entities from the initial user input use code similar to shown below. Please note this is only needed if you need information extracted from the initial user input, if you are prompting for information once the action is executed this part is not needed.

```
if template_entity in entities:
    template_entity = entities.get(template_entity)
else:
    template_entity = request_additional_info(chat_prompt, template_entity, f"The prompt you would like to show the user when prompting for the missing entity", allow_any=True)
```

Alternatively, in the else statement you could have a default value stored if one isn't provided instead of prompting for missing entity information.


### Current OS

The current OS of the user is stored in the os_name variable and can be passed in as a variable if you need to have variations of their code depending on their operating system.

Below is an example of how you can do this

```    
    if os_name == "Linux":

        result = subprocess.run(["ls", folder_query], stdout=subprocess.PIPE, text=True)
        output_widget.append(f"AI: Listed files in the current directory:\n{result.stdout}")
        
    elif os_name == "Windows":

        result = subprocess.run(["cmd.exe", "/c", "dir", folder_query], stdout=subprocess.PIPE, text=True)
        output_widget.append(f"AI: Listed files in the current directory:\n{result.stdout}")
            
    else:
        logging.debug("Unsupported OS")
```


### Exporting and importing of data between intents

Exporting and importing data between intents is something that needs to be explicitly defined within the function and the training data so that it is managed in a controlled manner. Imports and exports are also done independently so you can support one without supporting the other if you so wish. As a result, you can ensure your function is only being interacted with in the expected way. 

The data is shared between intents via the shared_data. You will need to determine what data you wish to import and/or export which will vary depending on your action.

So for example in the list_files action there is export functionality and knowing that if anyone was importing data from the action that they most likely are looking for the list of files, as a result it stores that list of files in shared_data.

Alternatively, in the create_file action there is import functionality and knowing that if anyone was importing to the action they most likely looking to create a file, it looks for the full filepath of where the file should be created. In the case of create_file there is also export functionality which also provides the full filepath should anything need to be done to the file after it is created. In this case the full file path was used for both the import and export functionality however it can be different data.


I have provided template of how you would import and export data for reference below.

**Import** 
```
    if "template_import" in entities:
        template_import = entities.get("create_file_import")
        template_import_data = shared_data.pop(0)
    else:
        create_file_data = ""
```

**Export**
```
    if "template_export" in entities:
        template_export = entities.get("list_files_export")
        if list_files_export == "export" or list_files_export == "exported":
            shared_data.append(result.stdout)
            return shared_data
```
You also have the option to test your code within Mykros without providing any training data and without running the update_data.py script. In folder path /custom_actions/debug_actions/debug there will be a file called debug_executor.py. 

You will then want to set DEBUG_MODE to true in  the intent_config.yml file. Once that is done, when you try and trigger any intent it will instead will trigger the DEBUG_MODE and run your code. There will also be informational messages displayed when open the chat window so that you have an indicator that you are in DEBUG_MODE. Once you are done testing, you will want to change the DEBUG_MODE flag back to false.

### Installing libraries in the portable conda environment

Should you need to use any libraries not already being used by Mykros, you will need to install them into the portable environment.

The easiest way would be to add the libraries to the custom_requirements.txt file and they will be installed the next time you launch Mkyros.

Alternatively you can do it without launching Mykros by using the commands below

**On Linux**
```
./portable_env/conda/bin/pip install sample_library
```
**On Windows**
```
.\portable_env\conda\Scripts\pip.exe install sample_library
```

Similarly, if you wish to uninstall a library from the portable environment you can use the commands below. You will also want to make sure that if you added the library to the custom_requirements.txt that you remove it or else it will re-install it next time you launch Mykros.

**On Linux**
```
./portable_env/conda/bin/pip uninstall sample_library
```
**On Windows**
```
.\portable_env\conda\Scripts\pip.exe uninstall sample_library
```

### <ins>Training Data</ins>

Next we need to create the training data. By default Mykros expects the training data to be in English. Should you wish to train your model on a language other than English you will need to update the language listed in the config.yml. Should you be creating the training data in English, or have already updated the config file we will start with creating the training data.

You will find a folder called data in the main directory, which contains a subfolder called nlu. Inside the nlu folder, there are 5 subfolders file_actions, misc_actions, system_actions, web_actions, word_actions. You should create a yml file that matches your intent name (for example, template_intent.yml) in the subfolder that best aligns with your custom action. The yml file is where the training data is stored along along with any custom regex should it be required.

A large amount of training data is not required. Typically, you have around 20 examples. However, the number of examples can vary depending on the diversity of triggers for the intent. For instance, the mute_computer intent uses only 7 examples, while open_bookmark has 47 examples. While requesting your computer to be muted is a simple request, opening the bookmark has multiple pieces of data that need to be extracted and thus requires more examples.

The training data should match the format below and include the intent, examples, and intent keywords. In the example below the intent is check_spelling and the intent is misspelled_word.

```
version: "3.1"

nlu:

- intent: check_spelling
  examples: |
    - Is [hapenning](misspelled_word) spelled correctly?
    - Please check the spelling of [recieve](misspelled_word).
    - Verify if [acomodate](misspelled_word) is spelled correctly.
    - Can you confirm the spelling of [definately](misspelled_word)?
    - I'm not sure if [existance](misspelled_word) is spelled right.
    - Is [occurence](misspelled_word) spelled correctly?
    - Please check if [recieve](misspelled_word) is spelled right.
    - Verify the spelling of [seperate](misspelled_word).
    - Can you confirm if [definately](misspelled_word) is spelled right?
    - I'm not sure if [existance](misspelled_word) is spelled correctly.
    - How do you spell [hapenning](misspelled_word)?
    - What is the correct spelling of [recieve](misspelled_word)?
    - Can you give me the proper spelling of [acomodate](misspelled_word)?
    - How do you spell [definately](misspelled_word)?
    - I'm unsure of the spelling of [existance](misspelled_word).
    - Could you tell me the correct spelling of [occurence](misspelled_word)?
    - What is the right way to spell [recieve](misspelled_word)?
    - Could you clarify the spelling of [seperate](misspelled_word)?
    - How do you spell [definately](misspelled_word) correctly?
    - I'm not sure of the spelling of [existance](misspelled_word). Can you help?

- regex: check_spelling_keywords
  examples: |
    - check|spelling|spell|spelled|misspelled
```


A sample yml file is in the template folder as well.

### Placeholders for special characters
Mykros supports 4 different placeholders for special characters that would otherwise be not supported. The placeholders are only needed in the training data. The user input, both entered and displayed, as well as processed by your custom action would directly use the special character.

Mykros will automatically convert the user input to the placeholder, so that it matches the training data. In addition, the actual special character is only ever displayed to the end user and not the placeholder to avoid any confusion.

```
__FSLASH__ = /
__PERCENT__ = %
__BSLASH__ = \
__DASH__ = -
```

These place holders are only needed in the training data. The user would input and any custom actions can use the special character directly.

So for example, should you need to add:
```
"List the files at [C:\Users\Bill\](folder_query)"
```
You would instead add:
```
"List the files at [C:__BSLASH__Users__BSLASH__Bill__BSLASH__](folder_query)"
```

Please keep in mind, this is only needed for above special characters. The other special characters are natively supported. For example ":" doesn't require a placeholder.

If you run into any other special characters not listed the cause issues please create an issue on the github page [here](https://github.com/scott-ca/mykros_framework/issues) listing the issue and I can create a placeholder for that special character.

&nbsp;

You may also include additional configuration options in the yml file shown below.


### Enabling importing data for your intent
```
- regex: create_file_import
  examples: |
    - import|imported
```
### Enabling exporting data for your intent
```
- regex: create_file_export
  examples: |
    - export|exported
```

By default, no entity configuration is required in the training data outside of being listed in the intent examples. However, you can include optional entity configuration as well. 

Below is the optional entity configuration.

### Limits entity extraction to only the included examples
```
- regex: browser
  examples: |
    - bookmark|firefox bookmark|brave bookmark
```
### Allows custom entity extraction. In the example below it will include any text after the word terminal as part of the entity
```
- regex: terminal_command
  examples: |
    - command|execute|terminal\s+(.*)
```
###Adds the non_word_flag to an entity. When enabled for an entity then if no entity is detected in the initial input, the intent that is the closest that uses the entity will assign the closest non-word. This is useful for detection of non-word names which are often used for company names or names of software**


### Assigns the closest non-word
```
- regex: misspelled_word
  examples: |
    - nonwords_flag
```


### <ins>Configuration files</ins>

There are four configuration files that you need to update:


**intent_config.yml:** This file is located in the main directory. Append your intent at the end of the file. The format should match the format below.

This is used for the /help function of Mykros as well as enabling of the intent itself. Any value other than true under enabled will treat the intent as disabled, in addition when you run update_data.py it will move the training data to the nlu_disabled folder. Should you later change it back to true, when you run the update_data.py it will enable the intent and move the training data back to the nlu folder.
```
template_intent:
  action: template_action
  summary: Brief summary of function.
  details: Detailed summary of the function
  enabled: true
```

Please note, you need to have at least 2 intents/actions enabled in the intent_config.yml to allow for proper detection of the intents. Otherwise you will get an nlu_fallback error.

**domain.yml:** This file is also in the main directory. Here, you need to list the intent, action, and entity. The format should match below.

I have included a single intent and an actions and four different entities. The entity template_entity being the standard entity, import/export being optional if you want the functionality, and template_restricted_values being an example of an intent that you are restricting to specific values. The only required values that need to be added are the intent and action should you only need basic functionality.
```
version: "3.1"

intents:
  - template_intent

actions:
  - action_template

entities:
  - template_entity
  - template_entity_import:
      values:
        - import
        - imported
  - template_entity_export:
      values:
        - export
        - exported
  - template_restricted_values:
      values:
        - bookmark
        - firefox bookmark
        - brave bookmark


session_config:
  session_expiration_time: 60
  carry_over_slots_to_new_session: true
```


Once those changes you need to run update_data.py and then you are done.

To do this, execute the following command in your command prompt/terminal while in the main folder:

**On Linux**
```
./portable_env/conda/bin/python update_data.py
```
**On Windows**
```
.\portable_env\conda\python.exe update_data.py
```

This will enable/disable the various intents based on the information in the intent_config.yml file and ensure their respective training data is in the nlu or disabled_nlu folder.


## IMPORTANT NOTE

In the current implementation of intent linking, it operates as an all-or-nothing approach for any specific instance of user input. So if your user input contains 3 intents they all need to use the linking functionality or none of them need to. This will be updated in the future to allow a mixture of linking and non-linking. You can mix and match intents that offer and don't offer the functionality, just the usage is restricted to all of the intents or none of the intents in any given user input.



## Feedback

I am happy to hear any feedback including but not limited to any features that you may like to see added. I won't make any commitments to add any of the features, however I will review them and should time allow see which features I may be able to implement.


## License

The Mykros framework and Mykros assist are licensed with a Apache Software License (Apache-2.0), in short this means that it can be used by anyone for any purpose. 

<ins>Private use</ins>

If you are using Mykros solely for private use such as internally within a company or for personal use, you do not need to disclose any of the source code including any of your modifications.

<ins>Public use</ins>

If you distribute Mykros to the public—either as a compiled executable or through a public-facing web interface—your users are entitled to a copy of the source code, including any modifications you've made.

We recognize that your deployment may contain sensitive information you wish to keep private for privacy or security reasons. Therefore, you are not required to include the following files and folders:

**Folders:**
```
custom_actions
data
disabled_data
```
**Files:**
```
config.yml
conflict_groups.yml
custom_requirements.txt
domain.yml
intent_config.yml
requirements.txt
settings.yml
```

While we encourage open-sourcing the entire project, we do respect and understand the need and right to privacy should extend in both directions and thus only the core functionality needs to be included. The custom actions and their respective training data and your config/setting files are optional and don't need to be included.

If you're solely utilizing the custom actions and any files mentioned above, you can simply provide a link to the repository using the links below:

Mykros framework:
```
https://github.com/scott-ca/mykros/
```
Mykros assist:
```
https://github.com/scott-ca/mykros_assist/
```

<ins>Additional license information</ins>

Both the Mykros framework and Mykros assist currently heavy rely of the Rasa model (licensed under Apache-2.0), PySide2 library (licensed under the Lesser General Public License) for the GUI, and Argos Translate library (Licensed under MIT) for language translation.

**Rasa:** The project doesn't include the Rasa source code, except for configuration files used to build the model. The model is generated from those configuration files, while the remaining components such as the action server are not utilized.

The Rasa project can be found here: https://github.com/RasaHQ/rasa/

**Pyside2:** This library is used for the GUI component of Mykros and the project can be found here: https://download.qt.io/official_releases/QtForPython/

**Argos Translate** This library is used for language translations and is used to translate the user input to the language used in the model, training data, custom action allowing them to interact with these functions using their native language. The project can be found here https://github.com/argosopentech/argos-translate
