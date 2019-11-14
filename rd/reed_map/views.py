import os
from datetime import datetime
from dateutil.parser import parse

from django.shortcuts import render
from rd.data.get_data import (
    get_green_restaurant_data,
    get_reed_datas
)


def index(request):
    template = 'reed_map/index.html'

    green_restaurant = get_green_restaurant_data()
    reed_datas = get_reed_datas()

    context = {
        'green_restaurant': green_restaurant,
        'reed_datas': reed_datas
    }

    return render(request, template, context)
