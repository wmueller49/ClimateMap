from django.shortcuts import render
import geopandas
import pandas as pd
import datetime


def index(request):
    return render(request, "map.html")

def calculator(request):
    return render(request,'calculator.html')

def climate_map(request):
    return render(request, "climate_map.html")

def update_map(request):
    if request.method == POST:
        year = request.POST.get('year', '')

        world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))

        temp_data = pd.read_csv("data/GlobalLandTemperaturesByCountry2.zip")

        temp_data['dt'] = pd.to_datetime(temp_data['dt'])
        temp_data = temp_data[temp_data['dt'].dt.year == year]
        temp_data = temp_data.groupby('Country', as_index=False)['AverageTemperature'].mean()

        somaliland = world.loc[world['name'] == "Somaliland"]
        sudan = world.loc[world['name'] == "Sudan"]

        world = world.merge(temp_data, left_on='name', right_on='Country')
        world = pd.concat([world, somaliland])
        world = pd.concat([world, sudan])

        world.loc[world["name"] == "Somaliland", "AverageTemperature"] = world[world['name'] == "Somalia"].AverageTemperature.values[0]
        world.loc[world["name"] == "Sudan", "AverageTemperature"] = world[world['name'] == "S. Sudan"].AverageTemperature.values[0]

        climate_map = world.explore(column='AverageTemperature')

        climate_map.save("map/templates/climate_map.html")

    return render(request, "map.html")

