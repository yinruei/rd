import os
import json
from datetime import datetime
from dateutil.parser import parse
from django.urls import reverse

from django.shortcuts import render
from rd.fetch_data.get_data import (
    get_green_restaurant_data,
    get_solitary_bee_hotel,
    get_water_quality_data
)
from django.conf import settings


def index(request, user=''):
    template = 'reed_map/index.html'
    if user == '':
        user = request.POST.get('user', 'None')

    bee_hotel_datas = get_solitary_bee_hotel()
    water_quality_data = get_water_quality_data()

    DATA_ROOT = os.path.join(settings.DATA_ROOT)
    with open(os.path.join(DATA_ROOT, 'green_restaurant.json'), 'r') as f:
        green_restaurant = json.load(f)

    with open(os.path.join(DATA_ROOT, 'reed_data.json'), 'r') as f:
        reed_datas = json.load(f)

    with open(os.path.join(DATA_ROOT, 'reed_river_all.json'), 'r') as f:
        reed_river_data = json.load(f)

    edited_datas = {}
    # if os.path.isfile(os.path.join(settings.BASE_DIR, 'new_data.csv')):
    #     with open(os.path.join(settings.BASE_DIR, 'new_data.csv'), 'r') as f:
    #         edited_datas = json.load(f)

    context = {
        'user': user,
        'green_restaurant': green_restaurant,
        'reed_datas': reed_river_data,
        'bee_hotel_datas': bee_hotel_datas,
        'map_tile': settings.MAP_TILE,
        'water_quality_data': water_quality_data,
        'edited_datas': edited_datas
    }

    return render(request, template, context)


def init_page(request):
    template = 'reed_map/init.html'
    context = {}

    return render(request, template, context)


def upload(request, edit_type='', edit_id='', user=''):
    template = 'reed_map/upload.html'
    context = {
        'edit_type': edit_type,
        'edit_id': edit_id,
        'user': user
    }

    return render(request, template, context)


def save_data(request):
    template = 'reed_map/thanks.html'
    contents = request.POST.get('contents', None)
    edit_type = request.POST.get('edit_type', None)
    edit_id = request.POST.get('edit_id', None)
    user = request.POST.get('user', None)

    context = {
        'user': user
    }

    file_content = user + ',' + edit_type + ',' + edit_id + ',' +contents
    _f = open('new_data.csv', 'w')
    _f.write(file_content)
    _f.close

    return render(request, template, context)
