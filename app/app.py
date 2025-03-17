from flask import Flask, request, jsonify
from dotenv import load_dotenv
from utils.prompt_generator import create_reading_activity_prompt, create_translation_activity_prompt, grade_translation_activity_prompt,create_listening_activity_prompt, grade_listening_activity_prompt
import json
from services.openaiservice import OpenAIService
from services.elevenlabsservice import ElevenLabsService
from flask_cors import CORS
from utils.file_utils import write_to_s3, generate_presigned_url
import os


load_dotenv()
app = Flask(__name__)

CORS(app)

ai_services = {
     "openai": OpenAIService(os.getenv("OPENAI_API_KEY")),
     "eleven_labs": ElevenLabsService(os.getenv("ELEVEN_LABS_API_KEY"))
}

@app.route("/echo")
def echo():
     return "echo"


@app.route("/<path:path>", methods=["OPTIONS", "GET", "POST", "PUT", "DELETE"])
def handle_options(path):
    response = app.make_response('')
    response.headers['Access-Control-Allow-Origin'] = '*'  # Or specify your domain
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@app.route("/translationGrade", methods=["POST"])
def create_translation_activity_grade():
    try:
        data = request.json
        print(data)
        language = data.get("language")
        source_text = data.get("source_text")
        target_text = data.get("target_text")
        reading_level = data.get("reading_level")
        model = data.get("model", "openai")

        prompt = grade_translation_activity_prompt(language, source_text, target_text, reading_level)

        response = ai_services[model].generate_response(prompt)

        print(response)

        if not response:
            return jsonify({"error": "Failed to generate response"}), 500
        return response 
    except Exception as e:
        return jsonify({"Error": str(e)}), 500


@app.route("/translationPage", methods=["POST"])
def create_translation_page():
    try :
        data = request.json
        source_language = data.get("source_language")
        reading_level = data.get("reading_level")
        target_language = data.get("target_language")
        model = data.get("model", "openai")

        prompt = create_translation_activity_prompt(source_language, target_language, reading_level)
        print(prompt)
        response = ai_services[model].generate_response(prompt)

        if not response:
            return jsonify({"error": "Failed to generate response"}), 500
        return response 
    except Exception as e:
        return jsonify({"Error": str(e)}), 500
    

@app.route("/listeningGrade", methods=["POST"])
def create_listening_page_grade():
    data = request.json

    original_text = data.get("original_text")
    answers = data.get("answers")
    model = data.get("model", "openai")

    print(original_text)
    print(str(original_text))

    prompt = grade_listening_activity_prompt(original_text, answers)
    print(prompt)
    response = ai_services[model].generate_response(prompt)

    if not response:
        return jsonify({"error": "Failed to generate response"}), 500

    return json.loads(response)



@app.route("/listeningPage", methods=["POST"])
def create_listening_page():
        data = request.json
        language = data.get("language")
        reading_level = data.get("reading_level")
        model = data.get("model", "openai")
        prompt = create_listening_activity_prompt(language, reading_level)
        response = ai_services[model].generate_response(prompt)

        if not response:
            return jsonify({"error": "Failed to generate response"}), 500
        
        print(response)
        response_dict = json.loads(response)

        main_text = response_dict["text"]

        
        url = write_to_s3(ai_services["eleven_labs"].generate_response(main_text, language))
        main_text_url = generate_presigned_url(url)

        print(main_text_url)

        fragments = []
        for sentence in response_dict["sentences"]:
            print(sentence)
            audio_file = ai_services["eleven_labs"].generate_response(sentence, language)
            fragments.append({"sentence": sentence, "audio": generate_presigned_url(write_to_s3(audio_file))})



        return jsonify({
            "title": response_dict["title"],
            "text": main_text,
            "audio": main_text_url,
            "fragments": fragments,
        })


@app.route("/readingPage", methods=["POST"])
def create_reading_page():
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

