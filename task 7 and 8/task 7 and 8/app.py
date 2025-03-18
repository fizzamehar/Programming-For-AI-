from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)
API_KEY = "900b473053ca4dd6ab4fa228afa0a050"  
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("articles", [])

@app.route('/news', methods=['GET'])
def news():
    articles = get_news()
    return jsonify(articles)

@app.route('/')
def home():
    articles = get_news()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
