from django.urls import path
from . import views

app_name = "videoapp"

urlpatterns = [
    path('video/<int:id>/', views.videoDetail, 'detail')
]