from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
<<<<<<< HEAD
    path('climate_map', views.climate_map, name='climate_map'),
    path('update_map', views.update_map, name='update_map'),

=======
    path('calculator',views.calculator, name='calculator')
>>>>>>> 7a37ee51b873260b296c836d5e32f1bfe47a75e7
]