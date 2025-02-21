from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
from retrieval import build_index
from langchain_ollama import OllamaEmbeddings
import os

app = Flask(__name__, template_folder="templates")
CORS(app)

INDEX, METADATA = build_index()
embedding_model = OllamaEmbeddings(model="nomic-embed-text")

@app.route("/")
def home():
    return render_template("index.html")

def retrieve(query, k=5):
    if INDEX is None or METADATA is None:
        return [{"content": "ขออภัย ขณะนี้ระบบไม่พร้อมใช้งาน"}]

    query_embedding = embedding_model.embed_query(query)
    query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

    distances, indices = INDEX.search(query_embedding, k)

    results = []
    for idx in indices[0]:
        if idx < len(METADATA):  
            results.append(METADATA[idx])
    return results

def query_llama2(prompt):
    try:
        import subprocess
        full_prompt = f"ตอบคำถามเป็นภาษาไทยเท่านั้น:\n{prompt}"  # ✅ กำหนดให้ตอบภาษาไทย
        result = subprocess.run(["ollama", "run", "llama2", prompt], capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return f"เกิดข้อผิดพลาด: {e}"

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query_text = data.get('query', '')

    retrieved_context = retrieve(query_text, k=5)
    context_text = "\n".join([doc['content'] for doc in retrieved_context])

    prompt = f"ข้อมูล:\n{context_text}\n\nคำถาม: {query_text}\nคำตอบ:"
    answer = query_llama2(prompt)

    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
