import requests

# This is where you find functionality for adding cities to the database and home page.

def validate_city(city_name):
    # Returns two values, the first is if is valid or not, the second is the weather data.

    # We use the same API and API key from script.js.

    api_key = 'BP8GPRYV53UQ56SHJR5EFCJ77'
    url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/weatherdata/forecast?aggregateHours=24&contentType=json&unitGroup=metric&locationMode=single&key={api_key}&locations={city_name}'
    
    try:
        response = requests.get(url, timeout=10)
        
        # Ensure that the response is successful, othererwise return False.

        if response.status_code != 200:
            return False, None
            
        data = response.json()
        
        # Check if the API returned valid data, otherwise we return False.

        if 'errorCode' in data or 'message' in data or 'location' not in data:
            return False, None
        
        # Extract the relevant parts.

        weather_data = {
            'temperature': data['location']['currentConditions']['temp'],
            'conditions': data['location']['values'][0]['conditions'],
        }
        
        # Prepare conditions variable so we can select the icon later.

        conditions = weather_data['conditions'].lower()
        
        weather_data['icon'] = select_weather_icon(conditions)
        return True, weather_data
    
    # If something goes wrong return False.

    except Exception:
        return False, None

def select_weather_icon(conditions):
    # Based on the conditions, we select the appropriate icon.
    # The icons cane be seen in static/weather-icons.
    # The list of all weather conditions can be found here:
    # https://docs.google.com/spreadsheets/d/1cc-jQIap7ZToVaEgiXEk_Aa6YVYjSObLV9PMe4oHrFg/edit?pli=1&gid=1769797687#gid=1769797687
    # I left out the ones that say 'type_x' because i don't know what they mean.

    weather_to_icon_map = {
        # Clear conditions.

        'clear': 'clear-day.png',
        'clear conditions throughout the day': 'clear-day.png',
        
        # Cloudy conditions.

        'overcast': 'cloudy.png',
        'cloudy skies throughout the day': 'cloudy.png',
        'cloudier': 'cloudy.png',
        'cloudierpm': 'cloudy.png',
        'becoming cloudy in the afternoon': 'cloudy.png',
        
        # Partly cloudy.

        'variablecloud': 'partly-cloudy-day.png',
        'partly cloudy throughout the day': 'partly-cloudy-day.png',
        
        # Rainy.

        'rain': 'rain.png',
        'raindefinite': 'rain.png',
        'rainallday': 'rain.png',
        'rainam': 'rain.png',
        'rainpm': 'rain.png',
        'rainampm': 'rain.png',
        
        # Potential for rain.

        'rainchance': 'showers-day.png',
        'rainclearinglater': 'showers-day.png',
        'raindays': 'showers-day.png',
        'rainearlyam': 'showers-day.png',
        'rainlatepm': 'showers-day.png',
        
        # Snowy.

        'snow': 'snow.png',
        'snowdefinite': 'snow.png',
        'snowallday': 'snow.png',
        'snowam': 'snow.png',
        'snowpm': 'snow.png',
        'snowampm': 'snow.png',
        
        # Potential for snow.

        'snowchance': 'snow-showers-day.png',
        'snowclearinglater': 'snow-showers-day.png',
        'snowdays': 'snow-showers-day.png',
        'snowearlyam': 'snow-showers-day.png',
        'snowlatepm': 'snow-showers-day.png',
        
        # Both rain and snow.

        'rainsnowallday': 'rain-snow.png',
        'rainsnowam': 'rain-snow.png',
        'rainsnowpm': 'rain-snow.png',
        'rainsnowampm': 'rain-snow.png',
        'rainsnowdefinite': 'rain-snow.png',
        
        # Potential for both rain and snow.

        'rainsnowchance': 'rain-snow-showers-day.png',
        'rainsnowclearinglater': 'rain-snow-showers-day.png',
        'rainsnowearlyam': 'rain-snow-showers-day.png',
        'rainsnowlatepm': 'rain-snow-showers-day.png',
        
        # Storms/thunder.

        'stormspossible': 'thunder.png',
        'stormsstrong': 'thunder.png',
        
        # Thunderstorm with rain.

        'thunder rain': 'thunder-rain.png',
        
        # Thunder showers.

        'thunder showers': 'thunder-showers-day.png',
        
        # Fog.

        'fog': 'fog.png',
    }
    
    # If none match fall back to the 'none' icon.

    icon = 'none.png'
    
    # Map the weather type to the icon name, then return.

    for weather_type, icon_name in weather_to_icon_map.items():
        if weather_type in conditions:
            icon = icon_name
            break
    
    # If we couldn't find an exact match, try a less exact match.

    if icon == 'none.png':
        if 'thunder' in conditions or 'storm' in conditions:
            if 'rain' in conditions:
                icon = 'thunder-rain.png'
            elif 'shower' in conditions:
                icon = 'thunder-showers-day.png'
            else:
                icon = 'thunder.png'
        elif 'rain' in conditions and 'snow' in conditions:
            if 'shower' in conditions:
                icon = 'rain-snow-showers-day.png'
            else:
                icon = 'rain-snow.png'
        elif 'rain' in conditions:
            if 'shower' in conditions:
                icon = 'showers-day.png'
            else:
                icon = 'rain.png'
        elif 'snow' in conditions:
            if 'shower' in conditions:
                icon = 'snow-showers-day.png'
            else:
                icon = 'snow.png'
        elif 'clear' in conditions or 'sun' in conditions:
            icon = 'clear-day.png'
        elif 'cloud' in conditions and 'partial' in conditions:
            icon = 'partly-cloudy-day.png'
        elif 'fog' in conditions or 'mist' in conditions:
            icon = 'fog.png'
        elif 'wind' in conditions or 'gust' in conditions:
            icon = 'wind.png'
        elif 'hail' in conditions:
            icon = 'hail.png'
        elif 'sleet' in conditions or 'freezing' in conditions:
            icon = 'sleet.png'
    
    return icon
