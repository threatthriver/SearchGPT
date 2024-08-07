import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for development

# Replace with your actual API key
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Create the model
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="You are developed by Aniket Kumar and your name is IntellijMind. You are a helpful and informative AI assistant, similar to Search GPT.",
)

def search_yahoo(query):
    url = f"https://search.yahoo.com/search?p={query}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []
    for result in soup.find_all('div', class_='algo-sr'):
        title_elem = result.find('h3')
        link_elem = result.find('a')
        if title_elem and link_elem:
            title = title_elem.text
            link = link_elem['href']
            results.append({"title": title, "link": link})

    return results

def get_model_response(prompt):
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        results = search_yahoo(query)

        if results:
            combined_results = "\n".join([f"{i+1}. {r['title']}\n   {r['link']}" for i, r in enumerate(results[:5])])
            model_prompt = f"Here are some search results:\n{combined_results}\n\nBased on these results, can you provide a concise summary and any key insights you find, similar to how Search GPT would respond?"
            model_response = get_model_response(model_prompt)

            # Split the response into lines
            response_lines = model_response.splitlines()

            return jsonify(response_lines)

        else:
            return jsonify(["No results found."])

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)