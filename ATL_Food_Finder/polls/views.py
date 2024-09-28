# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Restaurant
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Favorite
from django.views.decorators.http import require_POST



def search_restaurants(request):
    query = request.GET.get('q', '')  # Default to empty string if no query
    restaurants = Restaurant.objects.all()

    if query:
        restaurants = restaurants.filter(
            Q(name__icontains=query) |
            Q(cuisine_type__icontains=query) |
            Q(address__icontains=query)
        )
    #new below AND added the favorites to return!
    favorite_ids = request.session.get('favorites', [])
    favorites = Restaurant.objects.filter(id__in=favorite_ids)  # Fetch restaurants by their IDs

    return render(request, 'polls/search_results.html', {'restaurants': restaurants, 'query': query, 'favorites': favorites})

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
    #new
    favorite_ids = request.session.get('favorites', [])
    #new
    # Add a 'is_favorite' attribute to each restaurant
    for restaurant in restaurants:
        restaurant.is_favorite = restaurant.id in favorite_ids

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

#def favorites_list(request):
    # favorites = Favorite.objects.filter(user=request.user)
    # return render(request, 'polls/favorites_list.html', {'favorites': favorites})
    # return render(request, 'polls/favorites_list.html')
    # favorites = Favorite.objects.filter(user=request.user)
    # return render(request, 'polls/favorites_list.html', {'favorites': favorites})
def favorites_list(request):
    favorite_ids = request.session.get('favorites', [])
    favorites = Restaurant.objects.filter(id__in=favorite_ids)  # Fetch restaurants by their IDs
    return render(request, 'polls/favorites_list.html', {'favorites': favorites})

#new all below
#def add_to_favorites(request, restaurant_id):
    #restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    #Favorite.objects.get_or_create(user=request.user, restaurant=restaurant)
    #return redirect('search_restaurants')


@require_POST
def add_to_favorites(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)


    # Check if 'favorites' exists in session; if not, initialize it
    if 'favorites' not in request.session:
        request.session['favorites'] = []

    # Add restaurant ID to favorites if it's not already there
    if restaurant_id not in request.session['favorites']:
        request.session['favorites'].append(restaurant_id)
        request.session.modified = True  # Mark the session as modified

    #new below (used to be search_results)
    # new, this was old return redirect('map_view')
    #old: return redirect(request.META.get('HTTP_REFERER', 'map_view'))
    return HttpResponse(status=204)


#def remove_from_favorites(request, restaurant_id):
    #favorite = get_object_or_404(Favorite, user=request.user, restaurant_id=restaurant_id)
    #favorite.delete()
    #return redirect('favorites_list')

@require_POST
def remove_from_favorites(request, restaurant_id):
    # Check if 'favorites' exists in session
    if 'favorites' in request.session and restaurant_id in request.session['favorites']:
            request.session['favorites'].remove(restaurant_id)
            request.session.modified = True  # Mark the session as modified
    return HttpResponse(status=204)
    #old: return redirect('favorites_list')
