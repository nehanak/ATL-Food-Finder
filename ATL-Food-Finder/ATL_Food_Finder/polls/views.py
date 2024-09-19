# Create your views here.
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Restaurant
from django.db.models import Q
import math

def home(request):
    return render(request, 'home.html')

def search(request):
    return render(request, "search.html")

def search_restaurants(request):
    query = request.GET.get('query', '')
    cuisine = request.GET.get('cuisine', '')
    location = request.GET.get('location', '')
    price_range = request.GET.get('price_range', '')
    rating = request.GET.get('rating', '')
    user_lat = float(request.GET.get('lat', 0))
    user_lng = float(request.GET.get('lng', 0))

    # Query restaurants based on search criteria
    restaurants = Restaurant.objects.filter(name__icontains=query)
    
    if cuisine:
        restaurants = restaurants.filter(cuisine_type__icontains=cuisine)
    
    if location:
        restaurants = restaurants.filter(address__icontains=location)
    
    #if price_range:
        #restaurants = restaurants.filter(price_range=price_range)
    
    if rating:
        restaurants = restaurants.filter(rating__gte=rating)

    # Build response data list
    """
    results = []
    for restaurant in restaurants:
        # Calculate the distance between the user and the restaurant
        distance = haversine(user_lat, user_lng, restaurant.latitude, restaurant.longitude)
        results.append({
            'name': restaurant.name,
            'address': restaurant.address,
            'cuisine_type': restaurant.cuisine_type,
            'rating': restaurant.rating,
            'distance': round(distance, 2)  # Round to 2 decimal places
        })
    """

    # Return the results as JSON
    results = list(restaurants.values('name', 'cuisine_type', 'address',
                                      'rating')) #'price_range'))
    return JsonResponse({'results': results})

def autocomplete(request):
    query = request.GET.get('query', '')
    suggestions = list(Restaurant.objects.filter(name__icontains=query).values_list('name', flat=True)[:5])
    return JsonResponse({'suggestions': suggestions})


def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in miles (use 6371 for kilometers)
    R = 3959.87433

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences between the coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distance in miles
    distance = R * c
    return distance
