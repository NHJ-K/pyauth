from django.urls import path
from .views import my_view,callback

urlpatterns = [
    path('', my_view, name='my-view'),
    path('callback',callback),
]
