from ctypes import sizeof
from flask import Flask, jsonify, request, render_template, redirect, flash, session
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/api/cupcakes')
def get_all_cupcakes():
    """Get data about all cupcakes"""
    cupcakes = Cupcake.query.all()
    serialized = [cupcake.serialize() for cupcake in cupcakes]
    return jsonify(cupcakes=serialized)


@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    """Get data about a single cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    serialized = cupcake.serialize()
    return jsonify(cupcake=serialized)


@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Create a cupcake with flavor, size, rating and image data from the body of the request."""

    flavor = request.json['flavor']
    image = request.json['image']
    rating = request.json['rating']
    size = request.json['size']

    cupcake = Cupcake(flavor=flavor, image=image, rating=rating, size=size)
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)
