from dataclasses import dataclass

from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

import requests

from producer import publish

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://root:root@db/main'
CORS(app)

db = SQLAlchemy(app)

host_admin = 'http://host.docker.internal:8000/api/user'


@dataclass
class Product(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass
class ProductUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    product_id = db.Column(db.Integer)
    UniqueConstraint('user_id', 'product_id', name='user_product_unique')


@app.route('/api/products')
def index():
    return (Product.query.all())


@app.route('/api/products/<int:id>/like', methods=['POST'])
def like(id):
    req = requests.get(host_admin,verify=False)
    jsondata = req.json()
    try:
        productUser = ProductUser(user_id=jsondata['id'], product_id=id)
        db.session.add(productUser)
        db.session.commit()
        #event
        publish('product_liked', id)
    except:
        abort(400, 'you are alreadt liked this product')
        pass
    return jsonify({
        'message': 'success'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
