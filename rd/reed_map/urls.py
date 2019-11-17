""" URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.urls import path, re_path
from .views import index, init_page, upload, save_data

app_name = 'reed_map'

urlpatterns = [
    path('map/<str:user>/', index, name='map'),
    path('map/', index, name='map'),
    path('', init_page, name='init_page'),
    path('save_data/', save_data, name='save_data'),
    path('upload/<str:edit_type>/<str:edit_id>/<str:user>/', upload, name='upload'),
]
