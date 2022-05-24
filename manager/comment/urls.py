from django.contrib import admin
from django.urls import path, include
from report import views

app_name = 'report'
urlpatterns = [
    path('<int:video_type>/', views.comment_main, name = 'comment_main'),
    path('<int:comment_id>/update/', views.detail_comment, name = 'detail_comment'),
    path('<int:report_id>/delete/', views.delete_comment, name = 'delete_comment'),
]