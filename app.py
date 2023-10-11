"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, redirect, flash, jsonify
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "crocodile"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

app.app_context().push()
# ACCESS FLASK WITHIN IPYTHON AND HAVE SESSIONS

@app.route('/')
def home_page():
    """Render homepage."""
    return render_template('index.html')

@app.route('/api/cupcakes')
def view_all_cupcakes():
    """Returns json of all cupcakes in the database in format:
    {cupcakes: [{id,flavor,size,rating,image},...]}
    """
    cupcakes = [ cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes = cupcakes)

@app.route('/api/cupcakes/<int:id>')
def view_single_cupcake(id):
    """  Return data on specific cupcake.

    Returns JSON like:
        {cupcake: {id, flavor, rating, size, image}}
    """
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes', methods = ['POST'])
def create_cupcake():
    """ Adds a cupcake to the database and returns json of the cupcake:
    {cupcake:{id,flavor,size,rating,url}}
    """
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json.get('image', 'https://tinyurl.com/demo-cupcake')

    new_cupcake = Cupcake(flavor= flavor, size=size, rating=rating, image = image)
    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake = new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:id>', methods = ['PATCH'])
def update_cupcake(id):
    """Update cupcake from data in request. Return updated data.

    Returns JSON like:
        {cupcake: {id, flavor, rating, size, image}}
    """
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating) 
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods = ["DELETE"])
def delete_cupcake(id):
    """Delete cupcake and return confirmation message.

    Returns JSON of {message: "Deleted"}
    """
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = "Deleted")
