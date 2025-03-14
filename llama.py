from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from together import Together

app = Flask(__name__)

# Replace 'your_api_key_here' with your actual API key
client = Together(api_key="7e22ea9f261f762acf97e6f15da33309a34944605eed4c69402294de7c3c955c")

# Store conversation history
conversation_history = []

@app.route("/")
def index():
    # Serve the HTML file directly from the root folder
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Append user input to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Get AI response
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
        messages=conversation_history,
    )

    ai_response = response.choices[0].message.content

    # Append AI response to conversation history
    conversation_history.append({"role": "assistant", "content": ai_response})

    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(debug=True)