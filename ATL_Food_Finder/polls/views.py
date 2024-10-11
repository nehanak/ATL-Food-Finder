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

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Favorite
import json

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
@login_required(login_url='/login/')
def home_view(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'polls/home.html', {
        'favorites': favorites,
        'username': request.user.username  # Pass the username to the template
    })

def add_to_favorites(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON.'}, status=400)

        place_id = data.get('place_id')
        name = data.get('name')
        formatted_address = data.get('formatted_address')
        phone_number = data.get('phone_number')
        website = data.get('website')
        cuisine_type = data.get('cuisine_type')
        photo_url = data.get('photo_url')

        if not place_id or not name:
            return JsonResponse({'message': 'Missing required fields.'}, status=400)

        # Check if the restaurant is already a favorite
        is_favorite = Favorite.objects.filter(user=request.user, place_id=place_id).exists()

        if is_favorite:
            return JsonResponse({'message': f'{name} is already in your favorites.'}, status=400)
        else:
            Favorite.objects.create(
                user=request.user,
                place_id=place_id,
                name=name,
                formatted_address=formatted_address,
                phone_number=phone_number,
                website=website,
                cuisine_type=cuisine_type,
                photo_url=photo_url
            )
            return JsonResponse({'message': f'{name} has been added to your favorites!', 'success': True})

    return JsonResponse({'message': 'Invalid request method.'}, status=405)


def get_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)

    # Serialize the favorite objects into JSON format
    favorites_data = [{
        'place_id': fav.place_id,
        'name': fav.name,
        'formatted_address': fav.formatted_address,
        'phone_number': fav.phone_number,
        'website': fav.website,
        'cuisine_type': fav.cuisine_type,
        'photo_url': fav.photo_url
    } for fav in favorites]

    return JsonResponse({'favorites': favorites_data})

@login_required(login_url='/login/')
@csrf_exempt
def remove_from_favorites(request):
    if request.method == 'POST':  # or 'DELETE' if you prefer
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON.'}, status=400)

        place_id = data.get('place_id')
        name = data.get('name')  # You might want to send the name along as well for consistent messages

        if not place_id:
            return JsonResponse({'message': 'Missing place_id.'}, status=400)

        # Check if the restaurant is already a favorite
        try:
            favorite = Favorite.objects.get(user=request.user, place_id=place_id)
            favorite.delete()
            return JsonResponse({'message': f'{name} has been removed from your favorites.', 'success': True})
        except Favorite.DoesNotExist:
            return JsonResponse({'message': 'Restaurant not found in your favorites.', 'success': False})

    return JsonResponse({'message': 'Invalid request method.'}, status=405)
