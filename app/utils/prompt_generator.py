
def create_reading_activity_prompt(language, reading_level):
    """
        Creates a prompt for generating reading activities in a particular language at the specified reading level.
        Parameters: 
        language (str): the language the response shoul be in.
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
    


    
    

