import os
import json
from datetime import datetime
from dateutil.parser import parse

from django.shortcuts import render
from rd.fetch_data.get_data import (
    get_green_restaurant_data,
    # get_reed_datas,
    get_solitary_bee_hotel,
    get_water_quality_data
)
from django.conf import settings


def index(request):
    template = 'reed_map/index.html'
    user = request.POST.get('user', 'None')

    # green_restaurant = get_green_restaurant_data()
    # reed_datas = get_reed_datas()
    bee_hotel_datas = get_solitary_bee_hotel()
    water_quality_data = get_water_quality_data()

    DATA_ROOT = os.path.join(settings.DATA_ROOT)
    with open(os.path.join(DATA_ROOT, 'green_restaurant.json'), 'r') as f:
        green_restaurant = json.load(f)

    with open(os.path.join(DATA_ROOT, 'reed_data.json'), 'r') as f:
        reed_datas = json.load(f)

    with open(os.path.join(DATA_ROOT, 'reed_river_all.json'), 'r') as f:
        reed_river_data = json.load(f)

    context = {
        'user': user,
        'green_restaurant': green_restaurant,
        'reed_datas': reed_datas,
        'bee_hotel_datas': bee_hotel_datas,
        'map_tile': settings.MAP_TILE,
        'water_quality_data': water_quality_data,
        'reed_river_data': reed_river_data
    }

    return render(request, template, context)


def init_page(request):
    template = 'reed_map/init.html'
    context = {}

    return render(request, template, context)


def upload(request, edit_type=''):
    template = 'reed_map/upload.html'
    context = {
        'edit_type': edit_type
    }

    return render(request, template, context)
