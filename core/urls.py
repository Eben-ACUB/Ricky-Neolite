

from django.urls import path
from .views import *

app_name = 'core'

urlpatterns = [
    path('core/', search_courier, name='search_courier'),


]
