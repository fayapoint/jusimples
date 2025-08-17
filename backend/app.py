from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
CORS(app)  # Permite requisições de qualquer origem

# Simulação de dados jurídicos básicos
legal_data = [
    {
        "id": 1,
        "title": "Constituição Federal - Art. 5º",
        "content": "Todos são iguais perante a lei, sem distinção de qualquer natureza, garantindo-se aos brasileiros e aos estrangeiros residentes no País a inviolabilidade do direito à vida, à liberdade, à igualdade, à segurança e à propriedade.",
        "category": "direitos_fundamentais"
    },
    {
        "id": 2,
        "title": "Código Civil - Art. 1º",
        "content": "Toda pessoa é capaz de direitos e deveres na ordem civil.",
        "category": "direito_civil"
    },
    {
        "id": 3,
        "title": "CLT - Art. 7º",
        "content": "São direitos dos trabalhadores urbanos e rurais, além de outros que visem à melhoria de sua condição social.",
        "category": "direito_trabalhista"
    }
]

@app.route('/')
def home():
    return jsonify({"message": "API do JuSimples está funcionando!"})

@app.route('/api/search', methods=['POST'])
def search_legal():
    data = request.get_json()
    query = data.get('query', '').lower()
    
    if not query:
        return jsonify({"error": "Query não fornecida"}), 400
    
    # Busca simples nos dados simulados
    results = []
    for item in legal_data:
        if query in item['title'].lower() or query in item['content'].lower():
            results.append(item)
    
    return jsonify({
        "query": query,
        "results": results,
        "total": len(results)
    })

@app.route('/api/legal-data')
def get_legal_data():
    return jsonify(legal_data)

@app.route('/api/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')
    
    if not question:
        return jsonify({"error": "Pergunta não fornecida"}), 400
    
    # Simulação de resposta baseada em IA
    # Em uma implementação real, aqui seria feita a consulta ao LLM
    response = {
        "question": question,
        "answer": f"Com base na legislação brasileira, sobre '{question}', posso informar que este é um tema importante do direito brasileiro. Para uma resposta mais específica, recomendo consultar um advogado especializado.",
        "sources": [
            {
                "title": "Constituição Federal",
                "article": "Art. 5º",
                "relevance": 0.8
            }
        ]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

