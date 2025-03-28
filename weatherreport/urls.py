from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"), # Home page.
    path("delete/<str:city_name>", views.delete_city, name="delete_city"), # URL for the X buttons on the city cards that delete each city.
]