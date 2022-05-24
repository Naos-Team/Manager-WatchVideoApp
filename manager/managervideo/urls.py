from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'managervideo'
urlpatterns = [
    path('managervideo/<str:pk>/', views.managervideo, name='managervideo'),
]