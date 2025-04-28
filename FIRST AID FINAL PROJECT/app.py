from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama3-8b-8192",
    temperature=0.3
)

template = """
You are a First Aid Assistant. Provide clear, concise first aid guidance.
Rules:
1. Respond in 1-2 sentences
2. Focus on immediate actions
3. Only for true emergencies (like cardiac arrest, severe bleeding, unconsciousness, stroke, major trauma) say: "🚨 EMERGENCY: [Action]"
4. For minor issues (nausea, small cuts, mild burns) do not use emergency tag
5. If asked about medicines, suggest 1-2 common options with "Consult doctor first"

Examples:
- "Cool burn under running water for 10 mins"
- "🚨 EMERGENCY: Call 1122 immediately - patient is unconscious"
- "For pain: Paracetamol (consult doctor first)"
- "For nausea, sip water slowly and rest"

Current issue: {question}
"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | llm

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '').strip() 
    
    if not user_input:
        return jsonify({'message': "Please describe your first aid need"})

    try:
        response = chain.invoke({"question": user_input})
        return jsonify({'message': response.content})
    except Exception as e:
        return jsonify({'message': "Please describe your issue again"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)