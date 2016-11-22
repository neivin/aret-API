from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from passlib.apps import custom_app_context as pass_context

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
		return '<Crop: %r>' % self.crop_name

	@property
	def serialize(self):
		""" Return object in easily serializable format """
		return {
			'id': self.id,
			'crop_name': self.crop_name,
			'description': self.description
		}


class Farmer(db.Model):
	__tablename__ = "FARMERS"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	name = db.Column(db.String(40))
	phone = db.Column(db.String(20))
	password_hash = db.Column(db.String(64))
	region = db.Column(db.Integer)
	age = db.Column(db.Integer)


	def __repr__(self):
		return '<Farmer: %r>' % self.email

	def hash_password(self, password):
		self.password_hash = pass_context.encrypt(password)

	def verify_password(self, password):
		return pass_context.verify(password, self.password_hash)

	@property
	def serialize(self):
		return {
			'id': self.id,
			'email': self.email,
			'name': self.name,
			'phone': self.phone,
			'region': self.region,
			'age': self.age
		}

""" ROUTES """

""" FARMERS """
""" GET - Get list of farmers on some criteria """
""" GET - Check login for a farmer """
""" POST - Make a new farmer account """
""" PUT - Update farmer infor """

@app.route('/api/farmers/new', methods=['POST'])
def new_farmer():
	email = request.json.get('email')
	password = request.json.get('password')
	phone = request.json.get('phone')
	region = request.json.get('region')
	age = request.json.get('age')

	# email and password must be there
	if email is None or password is None:
		abort(400)

	# user already exists
	if Farmer.query.filter_by(email=email).first() is not None:
		abort(400)

	farmer = Farmer(email=email, phone=phone, region=region, age=age)
	farmer.hash_password(password)
	db.session.add(farmer)
	db.session.commit()

	return (jsonify({'email': farmer.email}), 201)


#@app.route('/api/farmers/login?u=<string: email>&p=<string: password>')
#def login_user(email, password):
#	pass





""" MASTER CROP LIST """
""" GET - Get the list of all crops """
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