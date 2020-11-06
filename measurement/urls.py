from django.contrib import admin
from django.urls import path, include
from .views import calculateDistanceView

app_name = 'measurement'

urlpatterns = [
    path('', calculateDistanceView, name="calculateView")
]
