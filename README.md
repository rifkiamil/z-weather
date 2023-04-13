# Weather Display

This project provides a simple web interface for displaying current weather data for the user's location. It consists of an HTML page that displays the weather data, and a RESTful API that retrieves the data from the [OpenWeatherMap](https://openweathermap.org/) API.

## Getting Started

To use this code, you'll need to create a `key.json` file containing your OpenWeatherMap API key. You can do this by following these steps:

1. Go to the [OpenWeatherMap website](https://home.openweathermap.org/users/sign_up) and sign up for an account (if you haven't already).
2. Once you're signed in, go to the [API Keys](https://home.openweathermap.org/api_keys) page and create a new API key.
3. Copy the API key and create a new file in the root directory of this project called `key.json`.
4. Paste the API key into the `key.json` file like this:

{
"key": "YOUR_API_KEY_HERE"
}

Replace `YOUR_API_KEY_HERE` with your actual API key.

Once you've set up your API key, you can run the project by opening the `weather.html` file in a web browser. The page will automatically display the current weather data for your location, retrieved from the OpenWeatherMap API via the `/weather` service.

## API Documentation

The `/weather` service provides a simple RESTful API for retrieving weather data in JSON format. To use the API, make a GET request to the `/weather` endpoint like this:

GET /weather


The service will return a JSON object containing the following properties:

- `temperature`: The current temperature in degrees Celsius.
- `humidity`: The current relative humidity in percent.
- `wind_speed`: The current wind speed in meters per second.

Here's an example response:

{
"temperature": 12.5,
"humidity": 60,
"wind_speed": 3.2
}


## License

You do you boo! 
