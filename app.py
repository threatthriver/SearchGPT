import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# API Key Configuration (using environment variables)
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")
genai.configure(api_key=api_key)

# Model Configuration
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
    system_instruction="You are a helpful and informative AI assistant.",
)

# Search Function
def search_web(query):
    """Performs a web search using Yahoo and returns the top 5 results."""
    url = f"https://search.yahoo.com/search?p={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        for result in soup.find_all('div', class_='algo-sr'):
            title_elem = result.find('h3')
            link_elem = result.find('a')
            if title_elem and link_elem:
                results.append({"title": title_elem.text, "link": link_elem['href']})
        return results[:5]
    except requests.exceptions.RequestException as e:
        print(f"Error during web search: {e}")
        return []

# Model Interaction Function
def get_ai_response(query, search_results):
    """Generates a response from the AI model based on the query and search results."""
    combined_results = "\n".join([f"{i+1}. {r['title']}\n   {r['link']}" for i, r in enumerate(search_results)])
    prompt = f"Here are some search results:\n{combined_results}\n\nBased on these results, can you provide a concise summary and any key insights you find?"
    try:
        response = model.generate_text(prompt)
        return response.splitlines()
    except Exception as e:
        print(f"Error during AI response generation: {e}")
        return ["An error occurred. Please try again later."]

# Flask Route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]
        search_results = search_web(query)
        if search_results:
            ai_response = get_ai_response(query, search_results)
            return jsonify(ai_response)
        else:
            return jsonify(["No results found."])
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)