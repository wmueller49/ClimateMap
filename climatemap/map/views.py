from django.shortcuts import render
import geopandas
import requests
from django.shortcuts import render, redirect
import openai
from .secret_key import API_KEY
import pandas as pd
import datetime

openai.api_key = API_KEY


def index(request):
    return render(request, "map.html")


def calculator(request):
    return render(request, "calculator.html")


def climate_map(request):
    return render(request, "climate_map.html")


def update_map(request):
    if request.method == POST:
        year = request.POST.get('year', '')

        world = geopandas.read_file(
            geopandas.datasets.get_path('naturalearth_lowres'))

        temp_data = pd.read_csv("data/GlobalLandTemperaturesByCountry2.zip")

        temp_data['dt'] = pd.to_datetime(temp_data['dt'])
        temp_data = temp_data[temp_data['dt'].dt.year == year]
        temp_data = temp_data.groupby('Country', as_index=False)[
            'AverageTemperature'].mean()

        somaliland = world.loc[world['name'] == "Somaliland"]
        sudan = world.loc[world['name'] == "Sudan"]

        world = world.merge(temp_data, left_on='name', right_on='Country')
        world = pd.concat([world, somaliland])
        world = pd.concat([world, sudan])

        world.loc[world["name"] == "Somaliland", "AverageTemperature"] = world[world['name']
                                                                               == "Somalia"].AverageTemperature.values[0]
        world.loc[world["name"] == "Sudan", "AverageTemperature"] = world[world['name']
                                                                          == "S. Sudan"].AverageTemperature.values[0]

        climate_map = world.explore(column='AverageTemperature')

        climate_map.save("map/templates/climate_map.html")

    return render(request, "map.html")


def bot(request):
    if request.method == 'POST':
        prompt = "I am a user of a climate map website where an interactive map shows me the carbon footprint of all countries over time. I will be asking questions regarding climate change and carbon footprint. You are a chatbot named ClimateBot on the website that is powered by gpt3. Your job is to provide me information about climate change and how I can reduce my carbon footprint." + \
            request.POST.get('prompt')
        response = openai.Completion.create(
            model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=1000)
        formatted_response = response['choices'][0]['text'][1:]
        context = {
            'formatted_response': formatted_response,
            'prompt': prompt
        }
        return render(request, "chatbot.html", context)
    else:
        return render(request, "chatbot.html")
