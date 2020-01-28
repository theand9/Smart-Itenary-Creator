from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('explore/', views.explore, name='explore'),
    path('itinerary/', views.itinerary, name="itinerary")
]
