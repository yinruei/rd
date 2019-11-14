import os
from datetime import datetime
from dateutil.parser import parse

from django.shortcuts import render
from rd.data.get_data import (
    get_green_restaurant_data
)


def index(request):
    template = 'reed_map/index.html'

    green_restaurant = get_green_restaurant_data()

    context = {
        'green_restaurant': green_restaurant
    }

    return render(request, template, context)
