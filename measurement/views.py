from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .utils import get_geo, get_center_coordinates, get_zoom, get_ip_address
import folium

# Create your views here.


def calculateDistanceView(request):
    obj = get_object_or_404(Measurement, id=1)
    distance = None
    destination = None
    
    form = MeasurementModelForm(request.POST or None)
    geolocator = Nominatim(user_agent='measurement')

    # ip = '72.14.207.99' 
    ip = '2409:4043:395:5427:e06b:a9f8:6a9f:b220'
    ip_ = get_ip_address(request)
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

    m = folium.Map(width=900, height=630, 
                    location=get_center_coordinates(l_latitude,l_longitude),)

    # Location Marker
    folium.Marker([l_latitude, l_longitude], tooltip="Click here for more", popup=city['city'], 
    icon=folium.Icon(color="purple")).add_to(m)


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

        # Folium Map Modification
        m = folium.Map(width=800, height=500, 
                location=get_center_coordinates(l_latitude,l_longitude,d_latitude, d_longitude),
                zoom_start=get_zoom(distance))

        # Location Marker 
        folium.Marker([l_latitude, l_longitude], tooltip="Click here for more", popup=city['city'], 
        icon=folium.Icon(color="purple")).add_to(m)

        # Destination Marker
        folium.Marker([d_latitude, d_longitude], tooltip="Click here for more", 
        popup=destination, icon=folium.Icon(color="green", icon='cloud')).add_to(m)


        # Draw the Line b/w location and destination

        line = folium.PolyLine(locations=[pointA, pointB], weight=5, color="blue")
        m.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()

    m = m._repr_html_()
    # distance = None

    context = {
        'distance':distance,
        'destination':destination,
        'form':form,
        'map':m
    }

    return render(request, 'measurement/main.html', context)