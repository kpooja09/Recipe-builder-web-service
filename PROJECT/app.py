from flask import Flask
from flask import render_template
import requests
import json
import xmltodict
from zeep import Client
import datetime


app = Flask(__name__, template_folder='template', static_folder='static')

# index element
@app.route('/')
def hello_world():
	return render_template('index.html')

# recipr search API returns the recipe for keyword
@app.route('/search/<food>')
def search(food):
	
	url = "https://api.spoonacular.com/recipes/search?apiKey=0d56c81e911b438596b11b79c6a56ebe"
	response = requests.request("GET", url, params = {"query": food})

	recipe_dtls = response.json()
	
	with open('./data/recipe_search.json', 'w') as outfile:
		json.dump(recipe_dtls, outfile)

	with open('./data/recipe_search.json','r') as f:
		recipe_dtls = json.load(f)

	recipe_id = recipe_dtls['results'][0]['id']
	recipe = get_ingredients(recipe_id)
	nval = get_nutrious_value(recipe['ingr'])
	return {"ing" :nval, "instruction": recipe['instructions']}

# nutriotion values for ingredients are fetched for the recipe
def get_nutrious_value(ingr):
	ingr_nval = list([])
	table_html = """<style>
					table, th, td {
					border: 1px solid black;
					border-collapse: collapse;
					}
					th, td {
					padding: 5px;
					text-align: left;    
					}
					</style>"""
	# displaying elements in table format
	table_html += "<table style='width:50%'><tr><th>Ingredient</th><th>Total Calories</th><th>Total Fat</th></tr>"
	for elements in ingr:
		table_html += "<tr>"
		url = "https://nutritionix-api.p.rapidapi.com/v1_1/search/" + elements

		querystring = {"fields":"nf_calories,nf_total_fat"}

		headers = {
		    'x-rapidapi-host': "nutritionix-api.p.rapidapi.com",
		    'x-rapidapi-key': "6561b33070mshc917405da5808d7p1e18ccjsn58920f3bf6eb"
		    }

		response = requests.request("GET", url, headers=headers, params=querystring)

		response = response.json()
		# print(response)
		with open('./data/data_ingredient_' + elements + '.json', 'w') as outfile:
		    json.dump(response, outfile)
		# table elements
		with open('./data/data_ingredient_' + elements + '.json', 'r') as f:
			data = json.load(f)
			for d in data['hits'][:1]:
				table_html += "<td>"+ elements + "</td>"
				table_html += "<td>"+ str(d['fields']['nf_calories']) + "</td>"
				table_html += "<td>"+ str(d['fields']['nf_total_fat']) + "</td>"
		table_html += "</tr>"
	table_html += "</table>"
	return table_html

# get the ingredients list for the recipe
def get_ingredients(recipe_id):

	url = "https://api.spoonacular.com/recipes/information?apiKey=cf4ab969a64043bc9558da8bda733b74"
	url = "https://api.spoonacular.com/recipes/" + str(recipe_id) + "/information?apiKey=0d56c81e911b438596b11b79c6a56ebe"
	 
	response = requests.request("GET", url)

	recipe_ingr = response.json()

	with open('./data/recipe_ingr.json', 'w') as outfile:
		json.dump(recipe_ingr, outfile)
	recipe = {}
	recipe['ingr'] = []
	with open('./data/recipe_ingr.json','r') as f:
		recipe_ingr = json.load(f)

		recipe['instructions'] = recipe_ingr['instructions']

		# first 20 elements are fetched
		for d in recipe_ingr['extendedIngredients'][:20]:
			recipe['ingr'].append(d['name'])
		# get_nutrious_value(ingr)
	return recipe

# gets current location for the user, This API is currently unavailble 
def get_mylocation():
	# lat= 0
	# lpn = 0
	# url = "https://api.ipgeolocation.io/ipgeo?apiKey=ce9217d1118e4c2cb4799c1ab9968b71"
	# ip = requests.get('http://ip.42.pl/raw').text
	# response = requests.request("GET", url, params= {"ip": ip})
	# my_location = response.json()
	# loc= str(my_location['latitude']) + "," +str(my_location['longitude'])
	loc = str(43.090606689453125) + "," +str(-77.64578247070312)
	return loc

# # get current weather using SOAP API
# @app.route('/weather')
# def get_currentweather():

# 	# lat, lon = get_mylocation().split(",")
# 	client = Client('https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php?wsdl')

# 	# SOAP request, parameters specify what all fields needed in the output
# 	response= client.service.NDFDgen(latitude=43.090606689453125,longitude=-77.64578247070312,
# 	                       startTime=datetime.datetime.now().date(),
# 	                      endTime=datetime.datetime.now().date()+ datetime.timedelta(days=2),product='time-series',
# 	                      Unit='m',weatherParameters={"maxt":1,"mint":1,
# 	                                                 "temp":1,"dew":0,"pop12":0,'qpf':0,
# 	                                                 "sky":0,"snow":1,'wspd':0,"wdir":0, "wx":0, 
# 	                                                  "waveh":0, "icons":0, "critfireo":0, 
# 	                                                  "dryfireo":0,'rh':0,'appt':0,'incw34':0,
# 	                                                 'incw50':0,'incw64':0,"cumw34":0,
# 	                                                 'cumw50':0,"cumw64":0,'conhazo':0,
# 	                                                 "ptornado":0,"phail":0,"ptstmwinds":0,
# 	                                                 "pxtornado":0,"pxhail":0,"pxtstmwinds":0,
# 	                                                  "ptotsvrtstm":0,"pxtotsvrtstm":0,"tmpabv14d":0,
# 	                                                 "tmpblw14d":0,'tmpabv30d':0,"tmpblw30d":0,
# 	                                                 "tmpabv90d":0,"tmpblw90d":0,"prcpabv14d":0,
# 	                                                 "prcpblw14d":0,"prcpabv30d":0,"prcpabv30d":0,
# 	                                                "prcpabv30d":0 ,"prcpblw30d":0,"prcpabv90d":0,
# 	                                                 "prcpabv90d":0,"prcpblw90d":0,"precipa_r":0,
# 	                                                 "sky_r":0,"temp_r":0,"wdir_r":0, "wspd_r":0, 
# 	                                                  "wgust":0, "iceaccum":0,"td_r":0,"wwa":0})

# 	# converting xml to json for parsing
# 	t = xmltodict.parse(response)
# 	with open('weather.json', 'w') as outfile:
# 	    json.dump(t, outfile)

# 	with open('weather.json','r') as f:
# 		weather_data = json.load(f)

# 	maximum_temp = weather_data['dwml']['data']['parameters']['temperature'][0]['value']
# 	minimum_temp = weather_data['dwml']['data']['parameters']['temperature'][1]['value']
# 	res = "Todays Weather: <br> Maximum Temp " + str(max(maximum_temp)),"degree Celcius, <br>Minimum Temp : "+ str(min(minimum_temp)), " degree Celcius <br><h4>Have a good one! </h4>"
# 	return {"weatherReport":res}

# # this connects with a API to get all the nearby grocerry stors.
# @app.route('/stores')
# def getStores():
# 	loc = get_mylocation()
	
# 	url ="https://dev.virtualearth.net/REST/v1/LocalSearch/?query=grocerry&key=AnIHk3-LY10J3oEqDpKLtOzs4nzZmFa0JOL4rvicXbFAZ5jYGseHv4LxB5uu4GEn"
# 	response = requests.request("GET", url,params = {"userLocation": loc})
# 	response = response.json()
# 	# print(response)
# 	with open('grocerry_stores.json', 'w') as outfile:
# 	    json.dump(response, outfile)
# 	stores_list = "<ol>"
# 	with open('grocerry_stores.json','r') as f:
# 		grocerry_Stores = json.load(f)
# 		# stores_list =list([])
# 		for stores in grocerry_Stores['resourceSets']:
# 			for s in stores['resources'][:7]:
# 				store = "<li><ul style = 'list-style-type:None'>"
# 				store += "<li><b>" + s['name'] + "</b></li>"
# 				store += "<li>" + s['Address']['formattedAddress']+ "</li>"
# 				store += "<li>" + s['PhoneNumber']+ "</li>"
# 				store += "<li>" + s['Website']+ "</li>"
# 				store += "</ul></li><br>"
# 				stores_list += store
# 	stores_list += "</ol>"
# 	return {'stores':stores_list}

# App run, debug mode true to avoid rerunning after changes
app.run(debug=True)
