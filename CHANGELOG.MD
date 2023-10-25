# CHANGELOG

All notable improvements, changes, and fixes to Mykros will be documented in this file.

## [Pre-release]

## [0.2.1] - 2023-10-25
### Major changes

- We've improved the accuracy for entity detection for recognizing longer, more complex phrases through two enhancements:

**Config/Model changes:** The CRFEntityExtractor was integrated, enhancing the system's capability to recognize longer phrases more effectively. This feature complements the existing featurizers including the DIETClassifier, which remains essential for identifying entities as well as assisting with detection should the input receive typos. In addition the word analyzer was added for the CountVectorsFeaturizer.

**Additional framework entity prioritization:**

The second enhancement added embedded functionality for entity prioritization that assists when multiple featurizers extract data for the same entity. This assists with better phrase detection, but also assists with ensuring correct entity is detection. This only occurs with multiple extractions of the same entity, it doesn't impact which entities are extracted between different entities.

The priority is given to the extraction that the most words within that specific entity. When entities have the same word counts, the system defaults to the one with the highest confidence score. An exception is made for the RegexEntityExtractor. The RegexEntityExtractor takes priorty regardless of the word count due to it being derived from the custom regex patterns you defined specifically for that entity. This prioritization of entities will also integrate with any additional featurizers you may enable in the config file as they are not the specific to just CRFEntityExtractor and DIETClassifier. The only requirement is that featurizer used provides a confidence score for the entity extraction.

### Minor changes/Bug fixes

- Developers now have the ability to access the translation functionality for their own custom actions. Once they import the module, they will only need to call the translate_custom function and provide the text to be translated and the 2 character code for the from and to languages. This is separate from the functionality that already existed to translate all input and/or output that the user can enable.

- Should you be working with translations that bypass English and require an intermediate language, for instance, translating from Spanish to Slovak you no longer need to manually change your settings to Spanish->English to download the model and then change it to English->Slovak to download the model. This process is now automatic and will download the required models to use the intermediate languages needed to complete the translation.

- When utilizing translation models, the downloaded zip of the model is no longer stored after it has been extracted. This reduces the disk space used for language models as only the model is stored now.

- Previously when linking multiple actions via using export/input it would occasionally allow too many intents if the intents weren't all part of the same conflict group. It now consider them as if they were part of the conflict group to ensure it allows the correct amount of intents. 

- Added version numbers to better track releases and changes in a more user readable format and to better allow for additioanl context.
 

## [0.2.0] - 2023-10-13

### Major changes

- Introduces comprehensive cross-language support, allowing you to interact with models in other languages. This feature can be configured to be used for only intent detection, all input, all output, or both input and output. This feature provides seamless interaction with the models and the custom_actions without needing to do any additional configuration to support the feature as it's native to the framework. 


### Minor changes/Bug fixes

- Added the __DASH__ placeholder and the relevant documentation for that placeholder as well as the other pre-existing placeholders to used in training data.

## [0.1.0] - 2023-10-05
- Initial pre-release version of Mykros, laying the foundation for the AI assistant framework. This version introduces the core functionalities and establishes the groundwork for future enhancements and features.
