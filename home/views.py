from django.shortcuts import render
from django.http import JsonResponse
from .models import *
# Create your views here.
from geopy.distance import  great_circle


def home(request):
    return render(request , 'home.html')





def api(request):
    restraunt_objs = Restraunt.objects.all()
    
    pincode = request.GET.get('pincode')
    km = request.GET.get('km')
    user_lat = None
    user_long = None
    
    if pincode:
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(int(pincode))
        user_lat = location.latitude
        user_long = location.longitude 
    
    
    payload = []
    for restraunt_obj in restraunt_objs:
        result = {}
        result['name'] = restraunt_obj.name
        result['image'] = restraunt_obj.image
        result['description'] = restraunt_obj.description
        result['pincode'] = restraunt_obj.pincode
        if pincode:
            first = (float(user_lat) , float(user_long))
            second = (float(restraunt_obj.lat) , float(restraunt_obj.lon))
            result['distance'] = int( great_circle(first , second).miles)
        
        payload.append(result)
        
        if km:
            if result['distance'] > int(km):
                payload.pop()
             
                
             
                    
        
        
    return JsonResponse(payload , safe=False)
    
    
    
    