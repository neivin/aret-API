from flask import Flask, request, abort, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/aret-3750'

heroku = Heroku(app)
db = SQLAlchemy(app)

# -----------------
# |     MODELS    |
# -----------------

class Crop(db.Model):
	__tablename__ = "CROPMASTERLIST"

	id = db.Column(db.Integer, primary_key=True)
	crop_name = db.Column(db.String(20), unique=True)
	description = db.Column(db.String(140))

	def __init__(self, name, desc):
		self.crop_name = name
		self.description = desc

	def __repr__(self):
		return '<Crop: %r>' %self.crop_name

	@property
	def serialize(self):
		""" Return object in easily serializable format """
		return {
			'id': self.id,
			'crop_name': self.crop_name,
			'description': self.description
		}


class User(db.Model):
	__tablename__="users"
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)

	def __init__(self, email):
		self.email = email

	def __repr__(self):
		return '<Email: %r>' % self.email


#routes

@app.route('/api/crops')
def get_all_crops():
	all_crops = Crop.query.all()
	serialized_crops = [crop.serialize for crop in all_crops]

	return jsonify({'crops': serialized_crops})

@app.route('/api/user/<int:id>')
def get_user(id):
	user = User.query.get(id)
	if not user:
		abort(400)
	return jsonify({ 'id': user.id, 'email': user.email})


if __name__ == 'main':
	app.debug = True
	app.run()