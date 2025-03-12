from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.prompt_generator import create_reading_activity_prompt
from services.openaiservice import OpenAIService
from flask_cors import CORS
import os


load_dotenv()
app = Flask(__name__)

CORS(app)

ai_services = {
     "openai": OpenAIService(os.getenv("OPENAI_API_KEY"))
}

@app.route("/echo")
def echo():
     return "echo"


@app.route("/translationExercise", methods=["POST"])
def get_translation_page():
    return "translation exercise"

@app.route("/listeningExercise", methods=["POST"])
def get_listening_page():
    return "listening"

@app.route("/readingPage", methods=["POST"])
def get_reading_page():
     try:
         data = request.json
         language = data.get("language")  # Default to OpenAI
         reading_level = data.get("reading_level")
         model = data.get("model", "openai")
         
         prompt  = create_reading_activity_prompt(language, reading_level)
         print(prompt)
         response = ai_services[model].generate_response(prompt)

         if not response:  # If response is empty or None, return an error
           return jsonify({"error": "Failed to generate response"}), 500
         
         return response


     except Exception as e:
          return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

