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
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('search/', views.search_restaurants, name='search_restaurants'),
    path('map/', views.map_view, name='map_view'),
    path('login/', auth_views.LoginView.as_view(template_name='polls/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='polls/login.html'), name='logout'),
    # You can keep this to have `/login/` as a URL too
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('add-to-favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('api/get-favorites/', views.get_favorites, name='get_favorites'),
    path('remove-from-favorites/', views.remove_from_favorites, name='remove_from_favorites'),

]
