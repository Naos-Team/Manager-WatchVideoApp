from django.urls import path
from . import views

app_name = "videoapp"

urlpatterns = [
    path('<str:id>/', views.updateVideo, name='update')
]