from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from passlib.apps import custom_app_context as pass_context
from datetime import datetime

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
	#records = db.relationship('Record', backref='FARMERS', lazy='dynamic')

	def __repr__(self):
		return '<Farmer: %r>' % self.email

	@staticmethod
	def hash_password(password):
		return pass_context.encrypt(password)

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

class Employee(db.Model):
	__tablename__="ARETEMPLOYEES"

	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(120), unique=True)
	name = db.Column(db.String(40))
	phone = db.Column(db.String(20))
	password_hash = db.Column(db.String(130))
	user_type = db.Column(db.Integer)
	region = db.Column(db.Integer)

	def __repr__(self):
		return '<ARETEmployee: %r>' % self.email

	@staticmethod
	def hash_password(password):
		return pass_context.encrypt(password)

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
			'user_type': self.user_type
		}

class Record(db.Model):
	__tablename__="FARMERCROPRECORDS"

	id = db.Column(db.Integer, primary_key=True)
	farmer_id= db.Column(db.Integer, db.ForeignKey('FARMERS.id'))
	crop_id= db.Column(db.Integer, db.ForeignKey('CROPMASTERLIST.id'))
	date_created=db.Column(db.DateTime)
	date_harvested=db.Column(db.DateTime)
	crop_yield = db.Column(db.Integer)

	@staticmethod
	def epoch_time(date):
		epoch = datetime.datetime(1970,1,1)
		delta_time = int((date - epoch).total_seconds())

		return delta_time

""" ROUTES """

""" FARMERCROPRECORDS """
# POST - Add a new record

# Create new record
# Must have: farmer email, crop_id
@app.route('/api/records/new', methods['POST'])
def new_record():
	email= request.json.get('email')
	crop_id= request.json.get('crop_id')

	if email is None or crop_id is None:
		abort(400)

	crop = Crop.query.filter_by(id=crop_id).first()
	farmer = Farmer.query.filter_by(email=email).first()

	if crop is None or farmer is None:
		abort(400) # crop does not exist or farmer does not exist

	new_rec = Record(farmer_id=farmer.id, crop_id=crop_id, date_created=datetime.now())
	db.session.add(new_rec)
	db.session.commit()

	return (jsonify({'farmer_id': new_rec.farmer_id,
					'email': farmer.email,
					'crop_id': crop_id,
					'crop_name':crop.name,
					'date_created': Record.epoch_time(new_rec.date_created),
					'date_harvested': None,
					'crop_yield': None}), 201)



""" ARET EMPLOYEES """
# GET - Check login details of farmer 
# GET - List all employees
# GET - List of employees filtered on som criteria

@app.route('/api/employees/all')
def get_employees():
	all_employees = Employee.query.all()
	serialized_employees = [emp.serialize for emp in all_employees]

	return jsonify({'employees': serialized_employees})

# GET - Pass in login information to get response
# In the format ?email=x@example.com&password=something
@app.route('/api/employees/login')
def login_employee():
	email = request.args.get('email')
	password = request.args.get('password')


	if email is None:
		abort(400)
	if password is None:
		abort(400)

	existing_emp = Employee.query.filter_by(email=email).first()
	
	if existing_emp is None:
		return make_response(jsonify({'status':'invalid email'}), 401)

	if not existing_emp.verify_password(password):
		return make_response(jsonify({'status':'invalid password'}), 401)

	return jsonify({
		'status': 'ok',
		'email':email
		})


# GET - Query farmers on some criteria
# Query terms: user_type, region
@app.route('/api/employees/query')
def query_employees():
	user_type = request.args.get('user_type')
	region = request.args.get('region')

	all_emps = Employee.query.all()

	if user_type is not None and region is not None:
		all_emps = Employee.query.filter_by(user_type=user_type, region=region).all()
	elif user_type is not None:
		all_emps = Employee.query.filter_by(user_type=user_type).all()
	elif region is not None:
		all_emps = Employee.query.filter_by(region=region).all()

	
	serialized_emps = [emp.serialize for emp in all_emps]

	return jsonify({'employees': serialized_emps})


""" FARMERS """
#""" GET - List of all farmers """
""" GET - Get list of farmers on some criteria """
""" GET - Check login for a farmer """ 
#""" POST - Make a new farmer account """
#""" PUT - Update farmer info """ 

@app.route('/api/farmers/all')
def get_farmers():
	all_farmers = Farmer.query.all()
	serialized_farmers = [farmer.serialize for farmer in all_farmers]

	return jsonify({'farmers': serialized_farmers})


# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"a2@test.com", "password":"password"}' https://shielded-cove-74710.herokuapp.com/api/farmers/new
@app.route('/api/farmers/new', methods=['POST'])
def new_farmer():
	email = request.json.get('email')
	name = request.json.get('name')
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

	farmer = Farmer(name=name, email=email, password_hash= pw_hash, phone=phone, region=region, age=age)
	
	db.session.add(farmer)
	db.session.commit()

	return (jsonify({'id': farmer.id, 'email': farmer.email}), 201)

# PUT - Update a farmer's information
# curl -i -H "Content-Type: application/json" -X PUT -d '{"email":"a@test.com", "name":"test name"}' https://shielded-cove-74710.herokuapp.com/api/farmers/update
@app.route('/api/farmers/update', methods=['PUT'])
def update_farmer():
	if not request.json:
		abort(400)

	email = request.json.get('email')
	name = request.json.get('name')
	password = request.json.get('password')
	phone = request.json.get('phone')
	region = request.json.get('region')
	age = request.json.get('age')

	existing_farmer = Farmer.query.filter_by(email=email).first()

	print "reached 2"
	# farmer doesn't exist
	if existing_farmer is None:
		print "no farmer"
		abort(400)

	if name is not None:
		existing_farmer.name = name

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
			'name': existing_farmer.name,
			'email': existing_farmer.email,
			'phone': existing_farmer.phone,
			'age': existing_farmer.age,
			'region': existing_farmer.region
		})


# GET - Pass in login information to get response
# In the format ?email=x@example.com&password=something
@app.route('/api/farmers/login')
def login_user():
	email = request.args.get('email')
	password = request.args.get('password')


	if email is None:
		abort(400)
	if password is None:
		abort(400)

	existing_farmer = Farmer.query.filter_by(email=email).first()
	
	if existing_farmer is None:
		return make_response(jsonify({'status':'invalid email'}), 401)

	if not existing_farmer.verify_password(password):
		return make_response(jsonify({'status':'invalid password'}), 401)

	return jsonify({
		'status': 'ok',
		'email':email
		})


# GET - Query farmers on some criteria
# Query terms: age, region
@app.route('/api/farmers/query')
def query_farmers():
	age = request.args.get('age')
	region = request.args.get('region')

	all_farmers = Farmer.query.all()

	if age is not None and region is not None:
		all_farmers = Farmer.query.filter_by(age=age, region=region).all()
	elif age is not None:
		all_farmers = Farmer.query.filter_by(age=age).all()
	elif region is not None:
		all_farmers = Farmer.query.filter_by(region=region).all()

	
	serialized_farmers = [farmer.serialize for farmer in all_farmers]

	return jsonify({'farmers': serialized_farmers})


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