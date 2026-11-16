from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ecommerce.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), default="General")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category
        }

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return jsonify({
        "message": "E-Commerce API is Running!",
        "developer": "Danyal - Backend Developer",
        "endpoints": {
            "GET /products": "Get all products",
            "GET /products/<id>": "Get single product",
            "POST /products": "Add product",
            "PUT /products/<id>": "Update product",
            "DELETE /products/<id>": "Delete product"
        },
        "total_products": Product.query.count()
    })

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify({
        "count": len(products),
        "saved_in": "ecommerce.db",
        "products": [p.to_dict() for p in products]
    })

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data.get('name'),
        price=data.get('price'),
        category=data.get('category', 'General')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added!", "product": new_product.to_dict()}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    db.session.commit()
    return jsonify({"message": "Product updated!", "product": product.to_dict()})

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)