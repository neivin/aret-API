# ARET API - Backend for CIS 3750 Project

## Crop Master List


### GET - Get all crops
URL: https://shielded-cove-74710.herokuapp.com/api/crops

required: none
returns: json object containing all crops recognized by the system

## Employees

### POST - New employee
URL: https://shielded-cove-74710.herokuapp.com/api/employees/new

adds a new ARET employee account to the database
required: email, password
returns: json object containing id, email and user type

### GET - Get the list of all employees
URL: https://shielded-cove-74710.herokuapp.com/api/employees/all

provides a list of employees
required: none
returns: json object containing all ARET employee accounts

### GET - Login as an employee
URL: https://shielded-cove-74710.herokuapp.com/api/employees/login?email=x@y.com&password=pass

authenticates the provided account information
possible status: ok, invalid email, invalid password
required: email, password
returns: json object containing status, email, and user type

### GET - query some criteria
URL: https://shielded-cove-74710.herokuapp.com/api/employees/query

queries the database to produce a list of ARET employees based on type and/or region
required: none
returns: json object containing all ARET employee accounts that satisfy the search criteria

## Farmers

### GET - List of all farmers
URL: https://shielded-cove-74710.herokuapp.com/api/farmers/all

returns: json object containing all farmer accounts in the database

### POST - new farmer
URL: https://shielded-cove-74710.herokuapp.com/api/farmers/new

adds a new farmer account to the database
required info: email, password
returns: json object containing farmer id, farmer email

### PUT -  update_farmer
URL: https://shielded-cove-74710.herokuapp.com/api/farmers/update

updates farmer account information based on information provided
required info: email
returns: updated json object

### GET - Login farmer
URL: https://shielded-cove-74710.herokuapp.com/api/farmers/login?email=x@y.com&password=pass

authenticates the provided account information
possible status: ok, invalid email, invalid password
required info: email, password
returns: login status, and farmer email in a json object

### GET - Query farmers on some creiteria
URL: https://shielded-cove-74710.herokuapp.com/api/farmers/query?age=56&region=2

queries the database to produce a list of farmers based on age and/or region
required: none
returns: json object with all farmers that satisfy the filter conditions

## Records

### POST - Make new crops 
URL: https://shielded-cove-74710.herokuapp.com/api/records/new
adds a new record to farmer's history
required: farmer email, crop_id
returns: json object containing all information for the new record

method: query_farmer_record()
https://shielded-cove-74710.herokuapp.com/api/records/farmer
queries the database for record history of a farmer
required: farmer email
returns: json object containing all records associated with that farmer