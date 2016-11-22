#!flask/bin/python

from flask import Flask
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request


app = Flask(__name__)


crops = [
    {
        'crop_id': 1,
        'farmer_id': 1,
        'mcrop_id': 1,
        'date_create': 'asdfasdf',
        'date_harvest': 'asdfasdfa',
        'crop_yield': 123123,
        'delete_flag': False
    },
    {
        'crop_id': 2,
        'farmer_id': 1,
        'mcrop_id': 1,
        'date_create': 'jlkjlkj',
        'date_harvest': 'ljkjkl',
        'crop_yield': 123123123123,
        'delete_flag': False
    }
]

#########################  Get full json list #########################


# crops
@app.route('/api/crops', methods=['GET'])
def get_crops():
	return jsonify({'crops': crops})

# master crop list
@app.route('/api/mastercrops', methods = ['GET'])
def get_mastercrops():
	return jsonify({'mastercrops': mastercrops})

# aret users
@app.route('/api/arets', methods = ['GET'])
def get_arets():
	return jsonify({'arets': arets})

# farmer users
@app.route('/api/farmers', methods = ['GET'])
def get_farmers():
	return jsonify({'farmers': farmers})

# research files
@app.route('/api/files', methods = ['GET'])
def get_files():
	return jsonify({'files': files})

#######################################################################


########### Get the table base on the primary key #######

# crops
@app.route('/api/crops/<int:crop_id>', methods = ['GET'])
def get_crop(crop_id):
	crop = [crop for crop in crops if crop['crop_id'] == crop_id]
	if len(crop) == 0:
		abort(404)
	return jsonify({'crop': crop[0]})

# master crop list
@app.route('/api/mastercrops/<int:mcrop_id>', methods = ['GET'])
def get_mastercrop(mcrop_id):
	mastercrop = [mastercrop for mastercrop in mastercrops if mastercrop['mcrop_id'] == mcrop_id]
	if len(mastercrop) == 0:
		abort(404)
	return jsonify({'mastercrop': mastercrop[0]})

# aret users
@app.route('/api/arets/<int:aret_id>', methods = ['GET'])
def get_aret(aret_id):
	aret = [aret for aret in arets if aret['aret_id'] == aret_id]
	if len(aret) == 0:
		abort(404)
	return jsonify({'aret': aret[0]})

# farmer users
@app.route('/api/farmers/<int:farmer_id>', methods = ['GET'])
def ger_farmer(farmer_id):
	farmer = [farmer for farmer in farmers if farmer['farmer_id'] == farmer_id]
	if len(farmer) == 0:
		abort(404)
	return jsonify({'farmer': farmer[0]})


# research files
@app.route('/api/files/<int:file_id>', methods = ['GET'])
def get_file(file_id):
	file = [file for file in files if file['file_id'] == file_id]
	if len(file) == 0:
		abort(404)
	return jsonify({'file': file[0]})


##########################################################

################ post a new json table #####################


# crops
@app.route('/api/crops', methods=['POST'])
def create_crop():
	if not request.json or not 'farmer_id' in request.json:
		abort(400)
	# if len(crops) == 0:
	# 	abort(404)
	crop = {
		'crop_id': crops[-1]['crop_id']+1,
		'farmer_id': request.json['farmer_id'],
		'mcrop_id': request.json.get("mcrop_id", 0),
		# 'mcrop_id': request.json['mcrop_id'],
		'date_create': request.json.get("date_create", "0"),
		'date_harvest': request.json.get("date_harvested", "0"),
		'crop_yield': request.json.get("crop_yield", 0),
		'delete_flag': False
	}
	crops.append(crop)
	return jsonify({'crop': crop}), 201


# master crop list
# aret users
# farmer users
# research files

######################################################


############### put a exist json table #################

# crops
@app.route('/api/crops/<int:crop_id>', methods = ['PUT'])
def update_crop(crop_id):
	crop = [crop for crop in crops if crop['crop_id'] == crop_id]
	if len(crop) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'farmer_id' in request.json and type(request.json['farmer_id']) is not int:
		abort(400)
	if 'mcrop_id' in request.json and type(request.json['mcrop_id']) is not int:
		abort(400)
	if 'date_create' in request.json and type(request.json['date_create']) is not unicode:
		abort(400)
	if 'date_harvest' in request.json and type(request.json['date_harvest']) is not unicode:
		abort(400)
	if 'crop_yield' in request.json and type(request.json['crop_yield']) is not int:
		abort(400)
	if 'delete_flag' in request.json and type(request.json['delete_flag']) is not bool:
		abort(400)
	crop[0]['farmer_id'] = request.json.get('farmer_id', crop[0]['farmer_id'])
	crop[0]['mcrop_id'] = request.json.get('mcrop_id', crop[0]['mcrop_id'])
	crop[0]['date_create'] = request.json.get('date_create', crop[0]['date_create'])
	crop[0]['date_harvest'] = request.json.get('date_harvest', crop[0]['date_harvest'])
	crop[0]['crop_yield'] = request.json.get('crop_yield', crop[0]['crop_yield'])
	crop[0]['delete_flag'] = request.json.get('delete_flag', crop[0]['delete_flag'])
	return jsonify({'crop': crop[0]})


# master crop list
# aret users
# farmer users
# research files

############################################################

################ delete a json table based on primary key ############

# crops
@app.route('/api/crops/<int:crop_id>', methods=['DELETE'])
def delete_crop(crop_id):
    crop = [crop for crop in crops if crop['crop_id'] == crop_id]
    if len(crop) == 0:
    	abort(404)
    crops.remove(crop[0])
    return jsonify({'Delete': crop})

# master crop list
@app.route('/api/mastercrops/<int:mcrop_id>', methods=['DELETE'])
def delete_mastercrop(mcrop_id):
    mastercrop = [mastercrop for mastercrop in mastercrops if mastercrop['mcrop_id'] == mcrop_id]
    if len(mastercrop) == 0:
    	abort(404)
    mastercrops.remove(mastercrop[0])
    return jsonify({'Delete': mastercrop})

# aret users
@app.route('/api/arets/<int:aret_id>', methods=['DELETE'])
def delete_aret(aret_id):
    aret = [aret for aret in arets if aret['aret_id'] == aret_id]
    if len(aret) == 0:
    	abort(404)
    arets.remove(aret[0])
    return jsonify({'Delete': aret})

# farmer users
@app.route('/api/farmers/<int:farmer_id>', methods=['DELETE'])
def delete_farmer(farmer_id):
    farmer = [farmer for farmer in farmers if farmer['farmer_id'] == farmer_id]
    if len(farmer) == 0:
    	abort(404)
    farmers.remove(farmer[0])
    return jsonify({'Delete': farmer})

# research files
@app.route('/api/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    file = [file for file in files if file['file_id'] == file_id]
    if len(file) == 0:
    	abort(404)
    files.remove(file[0])
    return jsonify({'Delete': file})

###################################################################

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(debug=True)