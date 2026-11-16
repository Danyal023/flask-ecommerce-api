from flask import Flask, jsonify

app = Flask(__name__)

# Sample E-commerce Data - Like Daraz products
products = [
    {"id": 1, "name": "Wireless Headphones", "price": 3500, "category": "Electronics"},
    {"id": 2, "name": "Running Shoes", "price": 5500, "category": "Fashion"},
    {"id": 3, "name": "Smart Watch", "price": 8000, "category": "Electronics"}
]

@app.route('/')
def home():
    return jsonify({"message": "Flask E-commerce API is Running!", "status": "success"})

@app.route('/products', methods=['GET'])
def get_products():
    return jsonify({"products": products, "count": len(products)})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)