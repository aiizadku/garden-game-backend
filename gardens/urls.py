from django.urls import path
from . import views

# .../gardens/
urlpatterns = [
    path("harvest/", views.harvest),
    path("plant/", views.plant),
    path("water/", views.water),
    path("water_all/", views.water_all),
    path("save/", views.save),
    path("load/", views.load),
    path("available_plants/", views.available_plants),
    path("set_is_new/", views.set_is_new),
]
