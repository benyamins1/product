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


@app.route("/")
def hello():
    return "<p>hello world!</p>"


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
