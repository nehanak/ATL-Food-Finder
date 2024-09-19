# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Restaurant
from django.db.models import Q

def search_restaurants(request):
    query = request.GET.get('q')
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