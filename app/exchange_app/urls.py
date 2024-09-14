from django.urls import path

from .views import exchange_get, exchange_post

urlpatterns = [
    path('', exchange_get, name='exchange_get'),
    path('calc/', exchange_post, name='exchange_post'),

]