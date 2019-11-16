import os
from datetime import datetime
from dateutil.parser import parse

from django.shortcuts import render
from rd.fetch_data.get_data import (
    get_green_restaurant_data,
    get_reed_datas,
    get_solitary_bee_hotel
)


def index(request):
    template = 'reed_map/index.html'
    user = request.POST.get('user', 'None')

    green_restaurant = get_green_restaurant_data()
    reed_datas = get_reed_datas()
    bee_hotel_datas = get_solitary_bee_hotel()

    context = {
        'user': user,
        'green_restaurant': green_restaurant,
        'reed_datas': reed_datas,
        'bee_hotel_datas': bee_hotel_datas
    }

    return render(request, template, context)


def init_page(request):
    template = 'reed_map/init.html'
    context = {}

    return render(request, template, context)