from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample data: list of FAQs
faqs = [
    {"id": 1, "question": "What is the color of an apple?", "answer": "Red."},
    {"id": 2, "question": "What makes tangerines sweet?", "answer": "High natural sugar content."},
    {"id": 3, "question": "How do berries stay so colorful?", "answer": "They contain natural pigments called anthocyanins."},
    {"id": 4, "question": "Why do avocados turn brown?", "answer": "Oxidation when exposed to air."},
]

# Helper function to find the FAQ by ID
def find_faq(faq_id):
    return next((faq for faq in faqs if faq['id'] == faq_id), None)

# GET /faqs - Fetch all FAQs
@app.route('/faqs', methods=['GET'])
def get_faqs():
    return jsonify(faqs), 200

# GET /faqs/<id> - Fetch a single FAQ by ID
@app.route('/faqs/<int:faq_id>', methods=['GET'])
def get_faq(faq_id):
    faq = find_faq(faq_id)
    if faq:
        return jsonify(faq), 200
    return jsonify({"error": "FAQ not found"}), 404

# POST /faqs - Create a new FAQ
@app.route('/faqs', methods=['POST'])
def add_faq():
    new_faq = request.json
    if "question" not in new_faq or "answer" not in new_faq:
        return jsonify({"error": "Invalid input"}), 400
    new_faq['id'] = max(faq['id'] for faq in faqs) + 1  # Automatically incrementing ID
    faqs.append(new_faq)
    return jsonify(new_faq), 201

# PUT /faqs/<id> - Update an existing FAQ by ID
@app.route('/faqs/<int:faq_id>', methods=['PUT'])
def update_faq(faq_id):
    faq = find_faq(faq_id)
    if not faq:
        return jsonify({"error": "FAQ not found"}), 404
    
    updated_data = request.json
    faq['question'] = updated_data.get('question', faq['question'])
    faq['answer'] = updated_data.get('answer', faq['answer'])
    
    return jsonify(faq), 200

# DELETE /faqs/<id> - Delete a FAQ by ID
@app.route('/faqs/<int:faq_id>', methods=['DELETE'])
def delete_faq(faq_id):
    faq = find_faq(faq_id)
    if faq:
        faqs.remove(faq)
        return jsonify({"message": "FAQ deleted"}), 200
    return jsonify({"error": "FAQ not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
