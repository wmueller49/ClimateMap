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
    if request.method == "POST":
        year = request.POST.get('year_val', '')

        print(f"YEAR: {year}")

        world = geopandas.read_file(
            geopandas.datasets.get_path('naturalearth_lowres'))

        temp_data = pd.read_csv("./map/data/GlobalLandTemperaturesByCountry.zip")

        temp_data.loc[temp_data['Country'] == "Burma", "Country"] = "Myanmar"
        temp_data.loc[temp_data['Country'] == "Bosnia And Herzegovina", "Country"] = "Bosnia and Herz."
        temp_data.loc[temp_data['Country'] == "Central African Republic", "Country"] = "Central African Rep."
        temp_data.loc[temp_data['Country'] == "Congo (Democratic Republic Of The)", "Country"] = "Dem. Rep. Congo"
        temp_data.loc[temp_data['Country'] == "Côte D'Ivoire", "Country"] = "Côte d'Ivoire"
        temp_data.loc[temp_data['Country'] == "Denmark (Europe)", "Country"] = "Denmark"
        temp_data.loc[temp_data['Country'] == "Dominican Republic", "Country"] = "Dominican Rep."
        temp_data.loc[temp_data['Country'] == "Equatorial Guinea", "Country"] = "Eq. Guinea"
        temp_data.loc[temp_data['Country'] == "Falkland Islands (Islas Malvinas)", "Country"] = "Falkland Is."
        temp_data.loc[temp_data['Country'] == "Central African Republic", "Country"] = "Central African Rep."
        temp_data.loc[temp_data['Country'] == "Czech Republic", "Country"] = "Czechia"
        temp_data.loc[temp_data['Country'] == "France (Europe)", "Country"] = "France"
        temp_data.loc[temp_data['Country'] == "Guinea Bissau", "Country"] = "Guinea-Bissau"
        temp_data.loc[temp_data['Country'] == "Macedonia", "Country"] = "North Macedonia"
        temp_data.loc[temp_data['Country'] == "Netherlands (Europe)", "Country"] = "Netherlands"
        temp_data.loc[temp_data['Country'] == "Palestina", "Country"] = "Palestine"
        temp_data.loc[temp_data['Country'] == "Solomon Islands", "Country"] = "Solomon Is."
        temp_data.loc[temp_data['Country'] == "Sudan", "Country"] = "S. Sudan"
        temp_data.loc[temp_data['Country'] == "Timor Leste", "Country"] = "Timor-Leste"
        temp_data.loc[temp_data['Country'] == "Trinidad And Tobago", "Country"] = "Trinidad and Tobago"
        temp_data.loc[temp_data['Country'] == "United Kingdom (Europe)", "Country"] = "United Kingdom"
        temp_data.loc[temp_data['Country'] == "United States", "Country"] = "United States of America"
        temp_data.loc[temp_data['Country'] == "Western Sahara", "Country"] = "W. Sahara"

        temp_data['dt'] = pd.to_datetime(temp_data['dt'])
        temp_data = temp_data[temp_data['dt'].dt.year == int(year)]
        temp_data = temp_data.groupby('Country', as_index=False)['AverageTemperature'].mean()

        somaliland = world.loc[world['name'] == "Somaliland"]
        sudan = world.loc[world['name'] == "Sudan"]

        world = world.merge(temp_data, left_on='name', right_on='Country')


        if world['name'].str.contains('Somaliland').any():
            world = pd.concat([world, somaliland])
            world.loc[world["name"] == "Somaliland", "AverageTemperature"] = world[world['name'] == "Somalia"].AverageTemperature.values[0]
        
        if world['name'].str.contains('Sudan').any():
            world = pd.concat([world, sudan])
            world.loc[world["name"] == "Sudan", "AverageTemperature"] = world[world['name'] == "S. Sudan"].AverageTemperature.values[0]

        climate_map = world.explore(column='AverageTemperature')

        climate_map.save("map/templates/climate_map.html")

        return render(request, "map.html", {"prev_year": year})


    return render(request, "map.html")


def bot(request):
    if request.method == 'POST':
        user_prompt = request.POST.get('prompt')
        prompt = "I am a user of a climate map website where an interactive map shows me the carbon footprint of all countries over time. I will be asking questions regarding climate change and carbon footprint. You are a chatbot named ClimateCompanion on the website that is powered by gpt3. Your job is to only provide me information about climate change and how I can reduce my carbon footprint." + \
            user_prompt
        response = openai.Completion.create(
            model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=1000)
        formatted_response = response['choices'][0]['text'][1:]
        context = {
            'formatted_response': formatted_response,
            'prompt': user_prompt
        }
        return render(request, "chatbot.html", context)
    else:
        return render(request, "chatbot.html")
