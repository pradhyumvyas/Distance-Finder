from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo
import folium

# Create your views here.


def calculateDistanceView(request):
    # obj = get_object_or_404(Measurement, id=1)
    
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurement')

    # ip = '72.14.207.99' 
    ip = '47.247.191.26'
    country,city,lat, lon = get_geo(ip)


    # print('location country ' , country)
    # print('location City ' , city)
    # print('location latitude and longitude ' , lat, lon)

    location = geolocator.geocode(city['city'])
    # print("###", location)

    # Location Coordinates 

    l_latitude = lat
    l_longitude = lon
    pointA = (l_latitude, l_longitude)

    # Initial Folium Map 

    m = folium.Map(width=800, height=500, location=pointA)


    if form.is_valid():
        instance = form.save(commit=False)
        destination_ = form.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)
        # print(destination)

        # Destination Coordination 
        d_latitude = destination.latitude
        d_longitude = destination.longitude

        pointB = (d_latitude, d_longitude)

        # Distance Calculation 
        distance = round(geodesic(pointA, pointB).km, 2)

        instance.location = location
        instance.distance = distance
        instance.save()

    context = {
        'distance':obj,
        'form':form,
        'map':m
    }

    return render(request, 'measurement/main.html', context)