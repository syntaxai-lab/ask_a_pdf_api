from flask import Flask, request, jsonify
from pymongo import MongoClient
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import fitz  # PyMuPDF for PDF handling
import logging
import os

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB setup
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["qa_database"]
collection = db["qa_collection"]

# Load Llama/Mistral model and tokenizer
MODEL_NAME = "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float16, device_map="auto")

def ask_llm(question: str) -> str:
    inputs = tokenizer(question, return_tensors="pt").to("cuda")
    output = model.generate(**inputs, max_new_tokens=200)
    return tokenizer.decode(output[0], skip_special_tokens=True)

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = "".join([page.get_text() for page in doc])
    return text

@app.route("/ask", methods=["POST"])
def ask_agent():
    data = request.get_json()
    question = data.get("question")
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    # Check if the question has been asked before
    cached_result = collection.find_one({"question": question})
    if cached_result:
        return jsonify({"question": question, "answer": cached_result["answer"]})
    
    # If not found, generate the answer
    answer = ask_llm(question)
    collection.insert_one({"question": question, "answer": answer})  # Cache the answer
    return jsonify({"question": question, "answer": answer})

@app.route("/query_db", methods=["POST"])
def query_db():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    result = collection.find_one({"question": query})
    if result:
        return jsonify({"question": query, "answer": result.get("answer", "No answer found")})
    else:
        return jsonify({"error": "No matching document"}), 404

@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    pdf_file = request.files["file"]
    pdf_path = os.path.join("uploads", pdf_file.filename)
    os.makedirs("uploads", exist_ok=True)
    pdf_file.save(pdf_path)
    text = extract_text_from_pdf(pdf_path)
    return jsonify({"filename": pdf_file.filename, "extracted_text": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
