"""
URL configuration for ATL_Food_Finder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from .views import map_view

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_restaurants, name='search_restaurants'),
    path('map/', map_view, name='map_view'),
    path('favorites/', views.favorites_list, name='favorites_list'),  # Add this line
    path('add_to_favorites/<int:restaurant_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:restaurant_id>/', views.remove_from_favorites, name='remove_from_favorites'),  # New path

]
