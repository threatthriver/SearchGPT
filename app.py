from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import asyncio

app = Flask(__name__)

# Load the API key from the file
with open("api_key.txt", "r") as file:
    api_key = file.read().strip()

# Configure the Google Generative AI SDK
genai.configure(api_key=api_key)

# Create the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 256,  # Limit the output response text length
    "response_mime_type": "text/plain",
}

# Instantiate the Generative Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction="You are IntellijMind, a friendly and helpful AI chatbot. Engage in casual conversation with the user, providing informative and supportive responses. Remember to be polite, positive, and engaging.",
)

# Start a new chat session
chat_session = model.start_chat(
    history=[
        # Initial chat history, if any
    ]
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
async def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        # Send the user's message to the model and get the response
        response = await chat_session.send_message_async(user_message)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
