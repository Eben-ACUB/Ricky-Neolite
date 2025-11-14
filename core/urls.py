

from django.urls import path
from .views import *

app_name = 'core'

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('core/', views.search_courier, name='search_courier'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='newsletter_subscribe'),
    path('logpage/', views.logpage, name='logpage'),
    # ... your other paths
]
