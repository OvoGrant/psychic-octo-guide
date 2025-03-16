
def create_reading_activity_prompt(language, reading_level):
    """
        Creates a prompt for generating reading activities in a particular language at the specified reading level.
        Parameters: 
        language (str): the language the response should be in.
        reading_level (str): how difficult the generated text should be to read.

        Returns:
        str: a prompt used for generating reading activities for users 
    """
    return  f"""
    You are being used as a language tutor that uses comprehensible input to teach its students. Your task is to create
    a medium length paragraph int the {language} at the {reading_level}. the following topics are considered You should create this passage with emphasis on 
    the parts of grammar and vocabulary that is taught most usefult at this level. Ensure structure of the text is generated
    with learning in mind. This means that naturality can be sacrificed for learning. repeated use of the same verb in 
    different tenses or adjectives with diferent genders will be useful. the following are examples you should imitate
    return the response as a json object in the form {{title: "title created for the text", text: "main text"}} """
    


def create_translation_activity_prompt(source_language, target_language, reading_level):
    """
        Creates a prompt for generating translation activities in a particular language at the specified level
        Parameters:
        language (str): the language the response should be in.
        reading_level (str): how difficult the generated activity should be to translate

        Returns:
        str: a prompt used for generating translation activities for users
    """
    return f"""
    You are being used as a language tutor that uses comprehensible input to teach its students. Your task is to create a
    medium length paragraph in the {source_language} that will be translated by the user into the {target_language}. The 
    Translation should be at the {reading_level}. return up to 10 sentence. Try to make the takes as diverse. Do not tell
    the same stories about going to the park or filled with cliches 

     **Response Format:** Return the response as a valid JSON object with the following structure:

    ```json
    {{
      "title": "Title of the text",
      "text": "Main text in {source_language}",
      "fragments": [
        {{
          "original_sentence": "Sentence from the main text in {source_language}",
          "translations": [
            "First translation into {target_language}",
            "Second translation into {target_language}"
          ]
        }},
        {{
          "original_sentence": "Another sentence from the main text in {source_language}",
          "translations": [
            "First translation into {target_language}",
            "Second translation into {target_language}"
          ]
        }}
      ]
    }}
    ```
    """
    

def grade_translation_activity_prompt(language, source_text, target_text, reading_level):
    """
        Creates a prompt for generating grades for translation activities
        Parameters:
        language (str): the language the translation is in
        source_text (str): the original text shown to the user
        target_text (str): the translation performed by the user
        reading_level (str): the current level of the user 

        Returns:
        str: a prompt used for gradeing translation activities
    """
    return f""" 
    You are being used as a strict grader for translation activities in {language} at the {reading_level}. 
    the following json object is in the format [{{original_sentence "the original sentence", "translation:["possible translations]}}]: {source_text}
    The follwing is a list of the translations the user created for each sentence {target_text}.
    You're job is to grade each sentence individually and generate a score out of {len(source_text) * 5}. each sentence can
    award a maximum of five points. 5 represents a perfect translation. take fewer marks off for small errors like accents

     **Response Format:** Return the response as a valid JSON object with the following structure:

    ```json
    {{
      "score": "score for the exercise",
      "total_points": "total points for the exercise",
      "strengths": [grammatical structure used correctly]
      "weaknesses": [grammatical structures used incorrectly]
    }}
    ```
    """