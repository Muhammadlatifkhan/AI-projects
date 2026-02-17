from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

client = Groq(api_key="USE YOUR OWN API KEY")

def process_message(message):
    prompt = f"""
You are a customer support AI.

Analyze the customer message and return ONLY the following 3 lines.
DO NOT repeat anything.
DO NOT add explanations.

FORMAT:
Category:
Sentiment:
Auto-Reply:

Customer Message:
"{message}"
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a precise customer support assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=120
    )

    return response.choices[0].message.content.strip()


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        user_message = request.form.get("message")
        if user_message:
            result = process_message(user_message)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
