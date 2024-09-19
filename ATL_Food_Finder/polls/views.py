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
    if query:
        restaurants = Restaurant.objects.filter(name__icontains=query)
    else:
        restaurants = Restaurant.objects.all()

    return render(request, 'polls/map_view.html', {'query': query, 'restaurants': restaurants})

