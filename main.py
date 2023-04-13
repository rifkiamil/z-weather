import json
import requests
from flask import Flask, request, abort, render_template

app = Flask(__name__)

app.config['url_prefix'] = 'http://127.0.0.1:5000'
app.config['EXPLAIN_TEMPLATE_LOADING'] = True
app.config['DEBUG'] = True



@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@app.route('/test/', methods=['GET'])
def test():
    current_url = request.url
    return render_template('index.html', current_url=current_url)

@app.route('/api/weather', methods=['GET'])
def weather():
    app.logger.info('/api/weather')
    if request.method != 'GET':
        abort(405) # Method Not Allowed
    with open('key.json') as f:
        api_key = json.load(f)['openweathermap']
    app.logger.info('API Key: %s', api_key)

    # Get city name from query string parameter
    city = request.args.get('search', '')
    app.logger.info('City: %s', city)

    # Get latitude and longitude of city from OpenWeatherMap Geocoding API
    geocoding_url = 'http://api.openweathermap.org/geo/1.0/direct'
    geocoding_params = {'q': city, 'limit': '', 'appid': api_key}
    geocoding_response = requests.get(geocoding_url, params=geocoding_params)
    if geocoding_response.status_code != 200:
        return {'error': 'An error occurred while fetching the geocoding data.'}
    geo_data = geocoding_response.json()[0]
    lat = geo_data['lat']
    lon = geo_data['lon']
    app.logger.info('Latitude: %s, Longitude: %s', lat, lon)

    # Get weather data from OpenWeatherMap API using latitude and longitude
    weather_url = 'https://api.openweathermap.org/data/2.5/weather'
    weather_params = {'lat': lat, 'lon': lon, 'appid': api_key}
    weather_response = requests.get(weather_url, params=weather_params)
    app.logger.info('API Request: %s', weather_response.url)

    if weather_response.status_code == 200:
        weather_data = weather_response.json()
        return weather_data
    else:
        return {'error': 'An error occurred while fetching the weather data.'}


@app.route('/weather')
def weather_page():
    cities = ['New York City', 'London', 'Paris']
    weather_data = []
    for city in cities:
        api_url = f"{app.config['url_prefix']}/api/weather?search={city}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            weather_data.append(data)
        else:
            app.logger.error(f"Error fetching weather data for {city}: {response.status_code}")
    return render_template('weather.html', weather_data=weather_data)

@app.route('/weather/<city>')
def city_weather(city):
    api_url = f'/api/weather?search={city}'
    weather_data = requests.get(api_url).text
    return render_template('weather.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)