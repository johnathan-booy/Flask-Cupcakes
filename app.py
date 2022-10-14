from ctypes import sizeof
import json
from flask import Flask, jsonify, request, render_template, redirect, flash, session
from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.route('/')
def show_homepage():
    """Show static homepage"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def list_cupcakes():
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
    image = request.json.get('image')
    rating = request.json['rating']
    size = request.json['size']

    cupcake = Cupcake(flavor=flavor, image=image, rating=rating, size=size)
    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    """Update a cupcake with the id passed in the URL and flavor, size, rating and image data from the body of the request."""

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json['flavor']
    cupcake.image = request.json.get('image', cupcake.image)
    cupcake.rating = request.json['rating']
    cupcake.size = request.json['size']

    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    """Delete cupcake with the id passed in the url"""

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
