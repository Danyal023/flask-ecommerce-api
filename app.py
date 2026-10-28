from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_product = Product(name=data['name'], price=data['price'], stock=data.get('stock', 0))
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added", "id": new_product.id}), 201

@app.route('/')
def home():
    return jsonify({"message": "E-Commerce Backend API | by Engr. Danyal Afzal - UOM | Islamabad"})

if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
