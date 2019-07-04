from flask import Flask, jsonify
import sqlite3
from datetime import date, timedelta
from bikram import samwat

app = Flask(__name__)

@app.route('/<string:veh_type>/<string:veh>/<int:cc>/<string:valid_upto>', methods = ['GET'])
def get(veh_type, veh, cc, valid_upto):
	x = calculate(veh_type, veh, cc, valid_upto)

	return jsonify({"Amount Due" : x[0], 'Valid Upto' : x[1]}), 200

def calculate(type, veh, cc, valid_upto):
	
	dates = list((valid_upto.split('-')))

	small_veh = ['CAR', 'JEEP', 'VAN', 'MICRO-BUS']
	power_veh = ['DOZER', 'EXCAVATOR', 'LOADER', 'ROLLER', 'TIPPER', 'CRANE', 'MINI-TIPPER', 'TRACTOR', 'POWER-TILLER', 'MINI-TRUCK', 'MINI-BUS', 'BUS', 'TRUCK']
	veh = veh.upper()
	tax = int()

	if(int(dates[2]) == 2076):
		year = '_' + '2075'

	else:
		year = '_' + dates[2]		

	if type == 'private':
		conn = sqlite3.connect('private.db')
			
	elif type == 'public':
		conn = sqlite3.connect('public.db')
			
	if veh == 'MOTORCYCLE':
		cursor = conn.execute('SELECT CC_BEG, CC_END, ' + year + ' FROM MOTORCYCLE')
			
		for row in cursor:
			if cc >= row[0] and cc <= row[1]:
				tax = row[2]
			
	elif veh in small_veh:
		cursor = conn.execute('SELECT CC_BEG, CC_END, ' + year + ' FROM SMALL_VEH')
					
		for row in cursor:
			if(row[0] <= cc and row[1] >= cc):
				tax = row[2]		
			
	elif veh in power_veh:
		cursor = conn.execute('SELECT TYPE, ' + year + ' FROM POWER_VEH')
			
		for row in cursor:
			if row[0] == veh:
				tax = row[1]

	temp = valid_upto
	valid_upto = samwat(int(dates[2]), int(dates[1]), int(dates[0]))
	cur_date = samwat.from_ad(date.today())

	validity = valid_upto + timedelta(days = 365)
	validity = validity.as_tuple()
	validity = str(validity[2]) + '-' + str(validity[1]) + '-' + str(validity[0])

	no_of_days_left = cur_date - valid_upto
	no_of_days_left = no_of_days_left.days

	if no_of_days_left <= 0:
		return 0, temp

	penalty_free_date = valid_upto.as_tuple()

	if(penalty_free_date[1] + 3 > 12):
		penalty_free_date = samwat(penalty_free_date[0]+1, 1, 1)
		penalty_free_date = penalty_free_date - timedelta(days = 1)

	else:
		penalty_free_date = samwat(penalty_free_date[0], penalty_free_date[1] + 3, penalty_free_date[2])

	if(penalty_free_date >= cur_date):
		return tax, validity

	days_exceeded = cur_date - penalty_free_date;
	days_exceeded = days_exceeded.days

	if days_exceeded <= 30:
		tax = tax + (0.05 * tax)

	elif days_exceeded <= 45:
		tax = tax + (0.1 * tax)

	else:
		cur_date = cur_date.as_tuple()

		if cur_date[0] == int(dates[2]):
			tax = tax + (0.2 * tax)

		else:
			tax = tax + (0.32 * tax)


	return tax, validity