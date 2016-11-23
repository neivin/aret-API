"""
TODO: verify email method for users
	region table, user type table (1 admin, 2 researcher, 3 ext group, 4 ext off/agent)
"""
from flask import Flask, request, abort, jsonify, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku
from passlib.apps import custom_app_context as pass_context
from datetime import datetime

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/aret-3750'

heroku = Heroku(app)
db = SQLAlchemy(app)


"""
 MODELS
 	Crop: 		id, crop_name, description
 	Farmer:		id, email, password_hash, name, region, age
 	Employee:	id, email, password_hash, name, region, user_type
 	Record:		id, farmer_id, crop_id, date_created, date_harvested, crop_yield
"""

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
		epoch = datetime(1970,1,1)
		delta_time = int((date - epoch).total_seconds())

		return delta_time

	@property
	def serialize(self):
		return {
			'id': self.id,
			'farmer_id': self.farmer_id,
			'crop_id': self.crop_id,
			'date_created': self.date_created,
			'date_harvested': self.date_harvested,
			'crop_yield': self.crop_yield
		}


""" ROUTES """

""" FARMERCROPRECORDS """
# POST - Add a new record <done>
# GET - Get records of a specific farmer <done>
# PUT - Harvest crop with yield done
# DELETE - Delete a record TODOOOOOOOOOOOOOOOOOOOOOOOOOOOO


# GET- Get every single record lol
@app.route('/api/records/all')
def get_all_records():
	all_records = Record.query.all()
	serialized_records = [rec.serialize for rec in all_records]

	return jsonify({'records': serialized_records})


# DELETE - Delete a record
@app.route('/api/records/delete/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
	if record_id < 1:
		abort(400)

	record = Record.query.filter_by(id=record_id).first()

	if record is None:
		abort(400)

	# prevent trying to convert Null to epoch
	harvest = None
	if record.date_harvested is not None:
		harvest =  Record.epoch_time(record.date_harvested)

	deleted_rec = jsonify({'id': record.id,
					'farmer_id': record.farmer_id,
					'crop_id': record.crop_id,
					'date_created': Record.epoch_time(record.date_created),
					'date_harvested': harvest,
					'crop_yield': record.crop_yield})

	db.session.delete(record)
	db.session.commit()

	return (deleted_rec, 200)



#PUT - harvest a crop with yield
@app.route('/api/records/update/<int:record_id>', methods=['PUT'])
def update_record(record_id):
	if record_id < 1:
		abort(400)

	record = Record.query.filter_by(id=record_id).first()

	# record does not exist
	if record is None:
		abort(400)

	crop = Crop.query.filter_by(id=record.crop_id).first()
	farmer = Farmer.query.filter_by(id=record.farmer_id).first()
		
	#no request
	if not request.json:
		abort(400)

	#crop yield not in json data
	crop_yield = request.json.get('crop_yield')
	if crop_yield is None:
		abort(400)

	record.crop_yield = crop_yield
	record.date_harvested = datetime.now()

	#commit data
	db.session.commit()

	return (jsonify({'id': record.id,
					'farmer_id': record.farmer_id,
					'farmer_email': farmer.email,
					'crop_id': record.crop_id,
					'crop_name':crop.crop_name,
					'date_created': Record.epoch_time(record.date_created),
					'date_harvested': Record.epoch_time(record.date_harvested),
					'crop_yield': record.crop_yield}), 201)

# Create new record
# Must have: farmer email, crop_id
# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"a@test.com", "crop_id":"2"}' https://shielded-cove-74710.herokuapp.com/api/records/new
@app.route('/api/records/new', methods=['POST'])
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

	return (jsonify({'id': new_rec.id,
					'farmer_id': new_rec.farmer_id,
					'farmer_email': farmer.email,
					'crop_id': crop_id,
					'crop_name':crop.crop_name,
					'date_created': Record.epoch_time(new_rec.date_created),
					'date_harvested': None,
					'crop_yield': None}), 201)


# Obtain records for a farmer by email
# GET - Get the records for a specific farmer
@app.route('/api/records/farmer')
def query_farmer_record():
	farmer_email = request.args.get('email')

	if farmer_email is None:
		abort(400)

	farmer = Farmer.query.filter_by(email=farmer_email).first()

	# if farmer does not exist
	if farmer is None:
		abort(400)

	all_records = Record.query.filter_by(farmer_id=farmer.id).all()

	serialized_records = [record.serialize for record in all_records]
	
	return jsonify({'records': serialized_records})



""" ARET EMPLOYEES """
# GET - Check login details of farmer 
# GET - List all employees
# GET - List of employees filtered on som criteria
# POST - Create account
# PUT - Update employee info

# PUT - Update employe information
# curl -i -H "Content-Type: application/json" -X PUT -d '{"email":"admin@aret.com", "name":"BIG BAD ADMINISTRATOR"}' https://shielded-cove-74710.herokuapp.com/api/employees/update
@app.route('/api/employees/update', methods=['PUT'])
def update_employee():
	if not request.json:
		abort(400)

	email = request.json.get('email')
	name = request.json.get('name')
	password = request.json.get('password')
	phone = request.json.get('phone')
	region = request.json.get('region')
	user_type = request.json.get('user_type')

	existing_emp = Employee.query.filter_by(email=email).first()

	# farmer doesn't exist
	if existing_emp is None:
		abort(400)

	if name is not None:
		existing_emp.name = name

	if password is not None:
		existing_emp.password_hash = Employee.hash_password(password)

	if phone is not None:
		existing_emp.phone = phone

	if region is not None:
		existing_emp.region = region

	if user_type is not None:
		if user_type < 1 or user_type > 4:
			abort(400)

		existing_emp.user_type = user_type

	db.session.commit()

	return jsonify({
			'id': existing_emp.id,
			'name': existing_emp.name,
			'email': existing_emp.email,
			'phone': existing_emp.phone,
			'user_type': existing_emp.user_type,
			'region': existing_emp.region
		})


# curl -i -H "Content-Type: application/json" -X POST -d '{"email":"testadmin@test.com", "password":"password", "user_type":1}' https://shielded-cove-74710.herokuapp.com/api/employees/new
# emp = app.Employee(name='Eddard Stark', email='eddard@aret.com', user_type=1, phone='1234567', region=1)
@app.route('/api/employees/new', methods=['POST'])
def new_employee():
	email = request.json.get('email')
	name = request.json.get('name')
	password = request.json.get('password')
	phone = request.json.get('phone')
	region = request.json.get('region')
	user_type = request.json.get('user_type')

	# email and password must be there
	if email is None or password is None or user_type is None:
		abort(400)

	# user already exists
	if Employee.query.filter_by(email=email).first() is not None:
		abort(400)

	# user_type is not 1-4
	if user_type < 1 or user_type > 4:
		abort(400)

	pw_hash = Employee.hash_password(password)

	emp = Employee(name=name, email=email, user_type=user_type, password_hash= pw_hash, phone=phone, region=region)
	
	db.session.add(emp)
	db.session.commit()

	return (jsonify({'id': emp.id, 'email': emp.email, 'user_type': emp.user_type}), 201)

# GET - list of all employees
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
		'email':email,
		'user_type': existing_emp.user_type
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
	if not request.json:
		abort(400)

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