## LOOKUP THE TAX DUE FOR THE A PARTICULAR VEHICLE

'GET /vehicle_registration_type/vehicle/cc/valid_upto'

**Valid values for above arguments**
- 'vehicle_registration_type' : ['private', 'public']
- 'vehicle' : ['motorcycle', 'CAR', 'JEEP', 'VAN', 'MICRO-BUS', 'DOZER', 'EXCAVATOR', 'LOADER', 'ROLLER', 'TIPPER', 'CRANE', 'MINI-TIPPER', 'TRACTOR', 'POWER-TILLER', 'MINI-TRUCK', 'MINI-BUS', 'BUS', 'TRUCK']
- 'cubic_centimeter_capacity' : applicable integer value for the vehicle
- 'valid-upto' : The date upto which the tax was last paid. The date should of format 'dd-mm-yyyy' (Note: Use dashes "-" to seperate the days, months, and years)

**Response**

-'200 OK' on success

'''json
{
	'Amount Due' : 66000,
	'Valid Upto' : '18-3-2076'
}
'''
