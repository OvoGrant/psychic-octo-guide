from elevenlabs import play
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs


class ElevenLabsService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = ElevenLabs(api_key=api_key)

    def generate_response(self, prompt, language):
        """
            Queries Elevn labs endpoint using text

            Parameters:
                text (str): the text that will be submitted to the AI client
                
            Returns:
            str: message generated server
        """
        audio = self.client.text_to_speech.convert(
               text=prompt,
               voice_id="JBFqnCBsd6RMkjVDRZzb",
               model_id="eleven_turbo_v2_5",
               output_format="mp3_44100_128",
        )

        return audio