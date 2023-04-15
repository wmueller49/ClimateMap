from django.shortcuts import render
import geopandas


def index(request):
    return render(request, "map.html")

def climate_map(request):
    return render(request, "climate_map.html")

def update_map(request):
    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

    

    climate_map = world.explore()
    climate_map.save("map/templates/climate_map.html")

    return render(request, "map.html")

