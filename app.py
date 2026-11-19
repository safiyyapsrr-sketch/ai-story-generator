from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
import os


# Load environment variables from .env
load_dotenv()


# Create Flask application
app = Flask(__name__)


# Get Gemini API key
api_key = os.getenv("GEMINI_API_KEY")


# Check API key
if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )


# Create Gemini client
client = genai.Client(api_key=api_key)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Generate story
@app.route("/generate", methods=["POST"])
def generate():

    try:

        # Get data from frontend
        data = request.get_json()

        topic = data.get("topic", "")
        genre = data.get("genre", "Fantasy")
        characters = data.get("characters", "")
        setting = data.get("setting", "")
        mood = data.get("mood", "Exciting")
        length = data.get("length", "Medium")


        # Check topic
        if not topic.strip():

            return jsonify({
                "success": False,
                "error": "Please enter a story topic."
            }), 400


        # Create the AI prompt
        prompt = f"""
You are an expert creative fiction writer.

Create a completely original story based on the information below.

STORY TOPIC:
{topic}

GENRE:
{genre}

CHARACTERS:
{characters}

SETTING:
{setting}

MOOD:
{mood}

STORY LENGTH:
{length}


IMPORTANT INSTRUCTIONS:

- Give the story a creative and interesting title.
- Create meaningful characters.
- Make the story original.
- Keep the characters and events consistent.
- Have a clear beginning, middle, and ending.
- Match the requested genre.
- Match the requested mood.
- Use descriptive but easy-to-understand language.
- Make the story engaging.
- Do not explain the writing process.
- Return only the title and the story.
"""


        # Send prompt to Gemini
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )


        # Get the generated story
        story = response.text


        # Send story back to frontend
        return jsonify({

            "success": True,

            "story": story

        })


    except Exception as e:

        print("ERROR:", e)

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# Start Flask
if __name__ == "__main__":

    app.run(debug=True)