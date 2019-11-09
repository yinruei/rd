import os
from datetime import datetime
from dateutil.parser import parse

from django.shortcuts import render


def index(request):
    template = 'reed_map/index.html'

    context = {
    }

    return render(request, template, context)
