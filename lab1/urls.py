
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('insert', orm_insert, name='insert'),
    path('delete/<int:id_films>', delete, name='delete'),
    path('push', push, name='push'),
    path('get_api', get_api, name='get_api')
]
