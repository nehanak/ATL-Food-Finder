# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Restaurant
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import LoginForm, RegisterForm

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
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home/')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You now have an account!.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
def home_view(request):
    return render(request, 'polls/home.html')
