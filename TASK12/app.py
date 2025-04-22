import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

with open('intents.json', 'r', encoding='utf-8') as f:
    intents_data = json.load(f)
model = SentenceTransformer('all-MiniLM-L6-v2')
tags = []
patterns = []
responses = {}

for intent in intents_data['intents']:
    tags.append(intent['tag'])
    responses[intent['tag']] = intent['responses']
    for pattern in intent['patterns']:
        patterns.append((pattern, intent['tag']))

pattern_texts = [p[0] for p in patterns]
pattern_embeddings = model.encode(pattern_texts, normalize_embeddings=True)

dimension = pattern_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(pattern_embeddings)

def get_response(user_input):
    user_embedding = model.encode([user_input], normalize_embeddings=True)
    
    D, I = index.search(user_embedding, k=1)
    most_similar_idx = I[0][0]
    similarity_score = D[0][0]
    
    if similarity_score > 0.5:
        matched_tag = patterns[most_similar_idx][1]
        response_options = responses[matched_tag]
        return np.random.choice(response_options)
    else:
        return np.random.choice(responses['fallback'])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.form['message']
    bot_response = get_response(user_message)
    return jsonify({'response': bot_response})

if __name__ == '__main__':
    app.run(debug=True) 