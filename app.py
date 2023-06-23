from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///myshop.db"
db = SQLAlchemy(app)
CORS(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50), default="General")
    price = db.Column(db.Numeric(10, 2), nullable=False)


# @app.route("/")
# def hello():
#     return "<p>hello world!</p>"
    
@app.route('/')
#@app.route("/index")
@app.route("/product")
@app.route("/product/<id>")
def product(id=-1):
    if id == -1:
        products = Product.query.all()
    else:
        products = [Product.query.get(id)]
    return_data = []
    for product in products:
        return_data.append(
            {
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                ' category': product. category,
                'price': product.price
            })
    if id != -1:
        return jsonify(return_data[0])

    return jsonify(return_data)

# need to post a json like this one:
# {
#     "category": "News",
#     "content": "Hello this is content",
#     "image": "https://picsum.photos/id/139/300/300",
#     "title": "News 888888 is here"
#   }

# {
#     "category": "Toys",
#     "name": "Baby Jumper",
#     "price": 199.90,
#     "stock": 55
#   }

@app.route('/create_Product/<id>', methods=['POST'])
@app.route('/create_Product', methods=['POST'])
def create_product(id=-1):
    data = request.get_json()    
    # add new Product
    if id==-1:
        new_product =Product(name=data['name'], stock=data['stock'], category=data['category'],price=data['price'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully'})
    # else:
    # # update Product
    #     Product = Product.query.get(id)
    #     Product.name = data['name']
    #     Product.stock = data['stock']
    #     Product.category = data['category']
    #     Product.price = data['price']
    #     db.session.commit()
    #     return jsonify({'message': 'Product updated successfully'})


@app.route('/delete_product/<int:id>', methods=['DELETE'])
def delete_Product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Deleted successfully'})
    else:
        return jsonify({'message': f'Error deleting {id}'})



with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
