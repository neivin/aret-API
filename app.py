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
	password_hash = db.Column(db.String(130))
	region = db.Column(db.Integer)
	age = db.Column(db.Integer)


	def __repr__(self):
		return '<Farmer: %r>' % self.email

	@staticmethod
	def hash_password(password):
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
""" GET - List of all farmers """
""" GET - Get list of farmers on some criteria """
""" GET - Check login for a farmer """ 
""" POST - Make a new farmer account """ #done
""" PUT - Update farmer info """

@app.route('/api/farmers')
def get_farmers():
	all_farmers = Farmer.query.all()
	serialized_farmers = [farmer.serialize for farmer in all_farmers]

	return jsonify({'farmers': serialized_farmers})


# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"a2@test.com", "password":"password"}' https://shielded-cove-74710.herokuapp.com/api/farmers/new
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

	pw_hash = Farmer.hash_password(password)

	farmer = Farmer(email=email, password_hash= pw_hash, phone=phone, region=region, age=age)
	
	db.session.add(farmer)
	db.session.commit()

	return (jsonify({'email': farmer.email}), 201)

# PUT - Update a farmer's information
#
@app.route('/api/farmers/update', methods=['PUT'])
def update_farmer():
	
	if not request.json:
		abort(400)

	email = request.json.get('email')
	password = request.json.get('password')
	phone = request.json.get('phone')
	region = request.json.get('region')
	age = request.json.get('age')

	existing_farmer = Farmer.query.filter_by(email=email).first()

	# farmer doesn't exist
	if existing_farmer is None:
		abort(400)

	if password is not None:
		existing_farmer.password_hash = Farmer.hash_password(password)

	if phone is not None:
		existing_farmer.phone = phone

	if region is not None:
		existing_farmer.region = region

	if age is not None:
		existing_farmer.age = age

	db.session.commit()

	return jsonify({
			'id': existing_farmer.id,
			'email': existing_farmer.email,
			'phone': existing_farmer.phone,
			'age': existing_farmer.age,
			'region': existing_farmer.region
		})



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




""" Run app """
if __name__ == 'main':
	app.debug = True
	app.run()