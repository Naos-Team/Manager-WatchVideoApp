from django.contrib import admin
from django.urls import path, include
from report import views

app_name = 'report'
urlpatterns = [
    path('', views.report_main, name = 'report_main'),
    path('/<int:report_id>/', views.detail_report, name = 'detail_report'),
]