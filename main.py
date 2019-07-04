from flask import Flask, jsonify
import sqlite3
from datetime import date, timedelta
from bikram import samwat

app = Flask(__name__)

@app.route('/<string:vehicle_registration_type>/<string:vehicle>/<int:cubic_centimeter_capacity>/<string:valid_upto>', methods = ['GET'])

def get(vehicle_registration_type, vehicle, cubic_centimeter_capacity, valid_upto):
	x = calculate(vehicle_registration_type, vehicle, cubic_centimeter_capacity, valid_upto)

	return jsonify({"Amount Due" : x[0], 'Valid Upto' : x[1]}), 200

def calculate(vehicle_registration_type, vehicle, cubic_centimeter_capacity, valid_upto):
	
	dates = list((valid_upto.split('-')))

	small_vehicle = ['CAR', 'JEEP', 'VAN', 'MICRO-BUS']
	power_vehicle = ['DOZER', 'EXCAVATOR', 'LOADER', 'ROLLER', 'TIPPER', 'CRANE', 'MINI-TIPPER', 'TRACTOR', 'POWER-TILLER', 'MINI-TRUCK', 'MINI-BUS', 'BUS', 'TRUCK']
	vehicle = vehicle.upper()
	tax = int()

	if(int(dates[2]) == 2076):
		year = '_' + '2075'

	else:
		year = '_' + dates[2]		

	if vehicle_registration_type == 'private':
		database_link = sqlite3.connect('private.db')
			
	elif vehicle_registration_type == 'public':
		database_link = sqlite3.connect('public.db')
			
	if vehicle == 'MOTORCYCLE':
		cursor = database_link.execute('SELECT CC_BEG, CC_END, ' + year + ' FROM MOTORCYCLE')
			
		for row in cursor:
			if cubic_centimeter_capacity >= row[0] and cubic_centimeter_capacity <= row[1]:
				tax = row[2]
			
	elif vehicle in small_vehicle:
		cursor = database_link.execute('SELECT CC_BEG, CC_END, ' + year + ' FROM SMALL_VEH')
					
		for row in cursor:
			if(row[0] <= cubic_centimeter_capacity and row[1] >= cubic_centimeter_capacity):
				tax = row[2]		
			
	elif vehicle in power_vehicle:
		cursor = database_link.execute('SELECT TYPE, ' + year + ' FROM POWER_VEH')
			
		for row in cursor:
			if row[0] == vehicle:
				tax = row[1]

	temp = valid_upto
	valid_upto = samwat(int(dates[2]), int(dates[1]), int(dates[0]))
	current_date = samwat.from_ad(date.today())

	validity = valid_upto + timedelta(days = 365)
	validity = validity.as_tuple()
	validity = str(validity[2]) + '-' + str(validity[1]) + '-' + str(validity[0])

	number_of_days_left = current_date - valid_upto
	number_of_days_left = number_of_days_left.days

	if number_of_days_left <= 0:
		return 0, temp

	penalty_free_date = valid_upto.as_tuple()

	if(penalty_free_date[1] + 3 > 12):
		penalty_free_date = samwat(penalty_free_date[0]+1, 1, 1)
		penalty_free_date = penalty_free_date - timedelta(days = 1)

	else:
		penalty_free_date = samwat(penalty_free_date[0], penalty_free_date[1] + 3, penalty_free_date[2])

	if(penalty_free_date >= current_date):
		return tax, validity

	days_exceeded = current_date - penalty_free_date;
	days_exceeded = days_exceeded.days

	if days_exceeded <= 30:
		tax = tax + (0.05 * tax)

	elif days_exceeded <= 45:
		tax = tax + (0.1 * tax)

	else:
		current_date = current_date.as_tuple()

		if current_date[0] == int(dates[2]):
			tax = tax + (0.2 * tax)

		else:
			tax = tax + (0.32 * tax)

	return tax, validity
