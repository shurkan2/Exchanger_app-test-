from django.urls import path

from .views import exchange_get, exchange_post, courses_table

urlpatterns = [
    path('', exchange_get, name='exchange_get'),
    path('calc/', exchange_post, name='exchange_post'),
    path('courses_table', courses_table, name='courses_table'),
]