from django.shortcuts import render
import geopandas
import requests
from django.shortcuts import render, redirect
import openai
from .secret_key import API_KEY

openai.api_key = API_KEY


def index(request):
    return render(request, "map.html")

def calculator(request):
    return render(request, "calculator.html")

def climate_map(request):
    return render(request, "climate_map.html")


def update_map(request):
    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres'))

    climate_map = world.explore()
    climate_map.save("map/templates/climate_map.html")

    return render(request, "map.html")

def bot(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=1000)
        formatted_response = response['choices'][0]['text']
        context = {
            'formatted_response': formatted_response,
            'prompt': prompt
        }
        return render(request, "chatbot.html",context)
    else:
        return render(request, "chatbot.html")
