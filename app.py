from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# DATABASE TABLE - Like Excel Sheet but for backend!
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), default='General')
    
    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": self.price, "category": self.category}

# Create Database file
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({"message": "Flask E-commerce API with DATABASE Running!", "database": "SQLite"})

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({"products": [p.to_dict() for p in products], "count": len(products), "saved_in": "ecommerce.db"})

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Name and price required"}), 400
    
    new_product = Product(
        name=data['name'],
        price=data['price'],
        category=data.get('category', 'General')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product saved to DATABASE!", "product": new_product.to_dict()}), 201

@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    db.session.commit()
    return jsonify({"message": "Product updated in DB!", "product": product.to_dict()})

@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": f"Product {product_id} deleted from DB!"})

if __name__ == '__main__':
    app.run(debug=True)