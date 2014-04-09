"""
Run this file once to setup your database.
"""

from pymongo import MongoClient
import json
import sys

client = MongoClient()
db = client.app
menu_items = db.menu_items
serveries = db.serveries
dishes = db.dishes
serv_dishes = db.serv_dishes

def main():
#############SERVERIES###################
	serv_info = [ 
		{	
			'name':'North Servery', 
			'serv_type': 0,
			'image':{
				'link':'./static/img/placeholder.jpeg'
			},    
			"location":{
				"latitude":29.721883,
		    "longitude":-95.396546
	    },
			'colleges_served': ['Martel', 'Jones', 'Brown'],
			'description': 'filler'
		},

		{	
			'name':'Seibel Servery, Abe and Annie', 
			'serv_type': 0,
			'image':{
				'link':'./static/img/placeholder.jpeg'
			},    
			"location": {
		      	"latitude":"29.716158",
		      	"longitude":"-95.398241"
		    },
			'colleges_served': ['Will Rice', 'Lovett'],
			'description': 'filler'
		},

		{	
			'name':'South Servery', 
			'serv_type': 1,
			'image':{
				'link':'./static/img/placeholder.jpeg'
			},
			"location":{
		     	"latitude":"29.715484",
		     	"longitude":"-95.401024"
		   	},
			'colleges_served': ['Hanszen', 'Wiess'],
			'description': 'filler'
		},

		{	
			'name':'West Servery', 
			'serv_type': 1,
			'image':{
				'link':'./static/img/placeholder.jpeg'
			},
		    "location":{
   			  "latitude":"29.721063",
   				"longitude":"-95.398481"
   			},
			'colleges_served': ['Duncan', 'McMurtry'],
			'description': 'filler'
		},

		{	
			'name':'Baker College Kitchen', 
			'serv_type': 2,
			'image':{
				'link':'./static/img/placeholder.jpeg'
			},
			"location":{ # baker college coordinates
    			"latitude":"29.716976",
    		  	"longitude":"-95.399289"
    		},
			'colleges_served': ['Baker'],
			'description': 'filler'
		},

		{	
			'name':'Sid Richardson Kitchen', 
			'serv_type': 2,
			'image':{
				'link':'./static/img/placeholder.jpeg'
			},
	    "location":{ # sid rich college coordinates
  		  	"latitude":"29.715162",
  		  	"longitude":"-95.398915"
  		},
			'colleges_served': ['Sid Richardson'],
			'description': 'filler'
		}
	]

	# fills servery times
	fill_servery(serv_info)
	for serv in serv_info:
		serveries.update({'name':serv['name']}, serv, True)
		print serv['name'] + " updated"


######################DISHES#################
	cursor = serveries.find({})
	# adds temporary foods
	dish_list = [{
		"name": "Mac and Cheese",
		"subscribers": [] # list of netIDs?
	},{
		"name": "Golden Catfish with Tartar Sauce",
		"subscribers": []
	},{
		"name": "Okra Garlic Tomato Stew",
		"subscribers": []
	},{
		"name": "Cheesecake",
		"subscribers": []
	}]

	for dish in dish_list:
		dishes.update({'name':dish['name']}, dish, True)
		print dish['name'] + " updated"


##############SERVERY DISHES#############
	serv_cursor = serveries.find({})
	dish_cursor = dishes.find({})
	# adds temporary foods
	serv_dish_list = [{
		"dish": dish_cursor.next(),
		"tags": ["gluten","soy","milk"], 
		"likes": 0,
		"servery": serv_cursor.next()["_id"]
	},{
		"dish": dish_cursor.next(),
		"tags": ["gluten","soy","milk","eggs","fish"],
		"likes": 0,
		"servery": serv_cursor.next()["_id"]
	},{
		"dish": dish_cursor.next(),
		"tags": ["gluten","soy"],
		"likes": 0,
		"servery": serv_cursor.next()["_id"]
	},{
		"dish": dish_cursor.next(),
		"tags": ["gluten","soy","milk","eggs"],
		"likes": 0,
		"servery": serv_cursor.next()["_id"]
	}]

	for serv_dish in serv_dish_list:
		serv_dishes.update({'dish':serv_dish['dish']}, serv_dish, True)
		print serv_dish['dish']['name'] + " updated"



	cursor = serv_dishes.find({})
	# adds temporary foods
	temp_menu = [{
		"meal": "lunch",
		"date": "2014-03-10",
		"dish": cursor.next()
	},{
		"meal": "lunch",
		"date": "2014-03-10",
		"dish": cursor.next()
	},{
		"meal": "lunch",
		"date": "2014-03-10",
		"dish": cursor.next()
	},{
		"meal": "dinner",
		"date": "2014-03-10",
		"dish": cursor.next()
	}]

	for item in temp_menu:
		menu_items.update({'dish':item['dish']}, item, True)
		print item['dish']['dish']['name'] + " updated"



def fill_servery(serv):
	"""
	fills in servery open times
	serv type 0 is North/Seibel
	serv type 1 is South/West
	serv type 2 is Sid/Baker

	serv is the servery JSON object and index is its position
	"""
	for index in xrange(len(serv)):
		serv_type = serv[index]["serv_type"]
		periods = {}

		# M-H
		for i in xrange(1,6):
			periods[str(i)] = {
				"breakfast": {
					"time_open": "0730",
					"time_close": "1030"
				},
				"lunch": {
					"time_open": "1130",
					"time_close": "1330"
				},
				"dinner": {
					"time_open": "1730",
					"time_close": "1930"
				}
			}

			# remove Friday dinners cause they are different for everyone
			if i == 5:
				del(periods[str(i)]["dinner"])

		# add other times for non Sid/Baker
		if serv_type in [0,1]:
			# add friday dinner
			periods["5"]["dinner"] = {
				"time_open": "1700",
				"time_close": "1900"
			}

			# adds sunday dinner and lunch
			periods["0"] = {
				"lunch": {
					"time_open": "1130",
					"time_close": "1400"
				},
				"dinner": {
					"time_open": "1700",
					"time_close": "1900"
				}
			}

			# adds Saturday lunch/dinner to North/Seibel
			if serv_type == 0:
				periods["6"] = {
					"breakfast": {
						"time_open": "0900",
						"time_close": "1100"
					},
					"lunch": {
						"time_open": "1130",
						"time_close": "1400"
					}
				}

		serv[index]["opening_hours"] = {
			"periods": periods
		}

		del serv[index]["serv_type"]


for arg in sys.argv:
	if arg == '--clean':
		serveries.remove()
	main()
