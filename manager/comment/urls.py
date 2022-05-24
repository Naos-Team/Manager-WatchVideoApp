from django.contrib import admin
from django.urls import path, include
from report import views

app_name = 'comment'
urlpatterns = [
    path('<int:video_type>/comment_home', views.report_home, name = 'comment_home'),
    path('comment_main/', views.report_main, name = 'comment_main'),
    path('<int:report_id>/delete/', views.delete_report, name = 'delete_comment'),
    # path('<int:report_id>/update/', views.detail_report, name = 'detail_report'),
]