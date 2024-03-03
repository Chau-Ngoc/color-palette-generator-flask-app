import json
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from openai import OpenAI

load_dotenv()

opai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

app = Flask(__name__)


def generate_colors_from_prompt(prompt, ai_client):
    instruction = f"""
You are a color palette generating bot. Your job is to understand the text prompt from user and then generate color palette from it.
The generated color palette should contain 2 to 8 colors

Q: Convert the following verbal description of a color palette to a list of hexadecimal color codes: What are the colors for a snowy mountain in golden hour?
A: ["#2e5a65", "#6a9099", "#a8b8b8", "#8e6d4e", "#79371f"]

Q: Convert the following verbal description of a color palette to a list of hexadecimal color codes: a warm summer night
A: ["#4B0082", "#FFBF00", "#DC143C", "#CD7F32", "#191970"]

### Desired Format: a valid JSON array of hexadecimal color codes

Q: Convert the following verbal description of a color palette to a list of hexadecimal color codes: {prompt}
A:
"""

    response = ai_client.completions.create(
        model="gpt-3.5-turbo-instruct", prompt=instruction, max_tokens=200
    )
    return json.loads(str.strip(response.choices[0].text))


@app.post("/generate-colors")
def generate_colors():
    prompt = request.get_json().get("prompt")
    colors = generate_colors_from_prompt(prompt, opai_client)
    return {"colors": colors}


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
