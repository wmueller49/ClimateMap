from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('climate_map', views.climate_map, name='climate_map'),
    path('update_map', views.update_map, name='update_map'),

]