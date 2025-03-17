from openai import OpenAI
client = OpenAI()
import openai

class OpenAIService:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_response(self, prompt):
        """
            Queries OpenAI endpoint using prompt

            Parameters:
                prompt (str): the prompt that will be submitted to the AI client
                
            Returns:
            str: message generated server
        """
        completion = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role":"user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content