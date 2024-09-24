# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Restaurant
from django.db.models import Q

def search_restaurants(request):
    query = request.GET.get('q', '')  # Default to empty string if no query
    restaurants = Restaurant.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(cuisine_type__icontains=query) |
            Q(address__icontains=query)
        )

    return render(request, 'polls/search_results.html', {'restaurants': restaurants, 'query': query})

def home(request):
    return redirect('search_restaurants')

def map_view(request):
    query = request.GET.get('q', '')
    cuisine = request.GET.get('cuisine', '')
    rating = request.GET.get('rating', '')
    price = request.GET.get('price', '')
    distance = int(request.GET.get('distance', 10))  # Default distance

    # Start with all restaurants
    restaurants = Restaurant.objects.all()

    # Filter by name
    if query:
        restaurants = restaurants.filter(name__icontains=query)

    # Filter by cuisine type
    if cuisine:
        restaurants = restaurants.filter(cuisine_type__icontains=cuisine)

    # Filter by rating (assuming you have a rating field)
    if rating:
        restaurants = restaurants.filter(rating__gte=int(rating))

    # Filter by price level (assuming you have a price_level field)
    if price:
        restaurants = restaurants.filter(price_level__lte=int(price))

    return render(request, 'polls/map_view.html', {
        'query': query,
        'cuisine': cuisine,
        'rating': rating,
        'price': price,
        'distance': distance,
        'restaurants': restaurants
    })
