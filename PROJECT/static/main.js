// This searches for a recipe and nutriotion values for it's ingredients
function searchFood(){

	food = document.getElementById('inputTxt').value
	
	var request = new XMLHttpRequest()

	// Open a new connection, using the GET request on the URL endpoint
	request.open('GET', 'http://127.0.0.1:5000/search/'+food, true)

	request.onload = function() {
	// Begin accessing JSON data here
		var data = JSON.parse(this.response)
		// ingr = data["ing"]
		document.getElementById("outputDiv").style.visibility="visible"
		getIngredients(data)
		getStores()
		getWeather()
	}

	// Send request
	request.send()

}

// It requests for the ingredients for the reicpe
function getIngredients(htmldt){
	var request = new XMLHttpRequest()

	// Open a new connection, using the GET request on the URL endpoint
	request.open('GET', 'http://127.0.0.1:5000/search', true)

	request.onload = function() {
	// Begin accessing JSON data here
		// var data = JSON.parse(this.response)
		// htmldt = data["weatherReport"]
		document.getElementById('ingr').innerHTML = htmldt['ing']
		document.getElementById('instrcution_recipe').innerHTML = htmldt['instruction']

	}

	// Send request
	request.send()
}

// // this gets the current weather
// function getWeather(){

	
// 	var request = new XMLHttpRequest()

// 	// Open a new connection, using the GET request on the URL endpoint
// 	request.open('GET', 'http://127.0.0.1:5000/weather', true)

// 	request.onload = function() {
// 	// Begin accessing JSON data here
// 		var data = JSON.parse(this.response)
// 		htmldt = data["weatherReport"]
// 		document.getElementById('weather_today').innerHTML = htmldt
// 	}

// 	// Send request
// 	request.send()

// }

// // this gets the nearby grocerry stores
// function getStores(){

// 	var request = new XMLHttpRequest()

// 	// Open a new connection, using the GET request on the URL endpoint
// 	request.open('GET', 'http://127.0.0.1:5000/stores', true)

// 	request.onload = function() {
// 	// Begin accessing JSON data here
// 		var data = JSON.parse(this.response)
// 		htmldt = data["stores"]
// 		document.getElementById('stores').innerHTML = htmldt
// 	}

// 	// Send request
// 	request.send()

// }