import json
import requests
from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return 'Hello, World!'

@app.route('/test', methods=['GET'])
def test():
    current_url = request.url
    return f'Hello Test The current URL is: {current_url}'

@app.route('/api/weather', methods=['GET'])
def weather():
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
        return 'An error occurred while fetching the geocoding data.'
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
        table_html = '<table>'
        for key, value in weather_data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    table_html += f'<tr><td>{key}.{subkey}</td><td>{subvalue}</td></tr>'
            else:
                table_html += f'<tr><td>{key}</td><td>{value}</td></tr>'
        table_html += '</table>'
        return table_html
    else:
        return 'An error occurred while fetching the weather data.'

if __name__ == '__main__':
    app.run(debug=True)
