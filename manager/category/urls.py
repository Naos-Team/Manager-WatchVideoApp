from django.contrib import admin
from django.urls import path, include
from . import views
app_name = 'category'
urlpatterns = [
    path('category/', views.category, name='category'),
]