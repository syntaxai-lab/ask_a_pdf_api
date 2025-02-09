from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Api setup
app = Flask(__name__)
api = Api(app)

# DB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["QA_database"]
collection = db[{"QA_collection"}]

# model details
MODEL_NAME = "mistralai/Mistral-7B-v1.1"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch)


# helper func
def ret_json(status, message, data=None):
    return jsonify({"status": status, "message": message, "data": data})


class Ask():
    pass


class Upload_pdf():
    pass


class Query_pdf():
    pass


# API endpoints
api.add_resource(Ask, '/ask')
api.add_resource(Upload_pdf, '/upload_pdf')
api.add_resource(Query_pdf, '/query_pdf')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
