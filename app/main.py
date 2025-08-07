from flask import Blueprint, request, jsonify
from .embedding import generate_embedding
from .qdrant_client import upsert_to_qdrant, query_qdrant

main_bp = Blueprint('main', __name__)

@main_bp.route('/add', methods=['POST'])
def add_text():
    data = request.get_json()
    text = data.get("text")
    if not text:
        return jsonify({"error": "Text is required"}), 400
    
    embedding = generate_embedding(text)
    upsert_to_qdrant(text, embedding)
    return jsonify({"message": "Text added successfully"})

@main_bp.route('/search', methods=['GET'])
def search_text():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query is required"}), 400
    
    embedding = generate_embedding(query)
    results = query_qdrant(embedding)
    return jsonify({"results": results})
