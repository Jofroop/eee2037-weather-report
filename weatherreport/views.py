from django.shortcuts import render, redirect
from .models import City
from .utils import validate_city # The function that gets the city.

def index(request):
    error_message = None
    success_message = request.session.pop('success_message', None)
    
    # Every time the page is loaded, update all the city weathers.

    update_all_cities_weather()
    
    if request.method == 'POST':
        city_name = request.POST.get('city', '')
        if city_name:
            # Check if city already exists to avoid duplicates
            if City.objects.filter(name=city_name).exists():
                # City already exists, set error message
                error_message = f"City ({city_name}) already exists in the list!"
            else:
                # Validate the city with the weather API
                is_valid, weather_data = validate_city(city_name)
                if is_valid:
                    # Create and save the city with weather data
                    city = City(
                        name=city_name,
                        temperature=weather_data['temperature'],
                        conditions=weather_data['conditions'],
                        icon=weather_data['icon']
                    )
                    city.save()
                    
                    # Store success message in session and redirect to prevent form resubmission
                    request.session['success_message'] = f"Successfully added {city_name}"
                    return redirect('/')
                else:
                    # City could not be found in the API
                    error_message = f"Could not find weather data for '{city_name}'. Please check the city name."
            
    # Get all cities from the database
    cities = City.objects.all()
    
    context = {
        'cities': cities,
        'error_message': error_message,
        'success_message': success_message
    }
    
    return render(request, 'weather-report.html', context)

def delete_city(request, city_name):
    # Find the city by name and delete it.

    deleted = City.objects.filter(name=city_name).delete()
    
    # If somethign was actually deleted, we set the success message.
    if deleted[0] > 0:
        request.session['success_message'] = f"Successfully deleted {city_name}"
    
    # Then back to the home page because we don't want the user to stay on /delete.
    return redirect('/')

def update_all_cities_weather():
    # Iterate through all cities and update.

    cities = City.objects.all()
    for city in cities:
        is_valid, weather_data = validate_city(city.name)
        if is_valid: # But only if valid.
            city.temperature = weather_data['temperature']
            city.conditions = weather_data['conditions']
            city.icon = weather_data['icon']
            city.save()