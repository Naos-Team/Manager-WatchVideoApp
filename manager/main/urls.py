from django.urls import path
from main import views
app_name = 'main'
urlpatterns = [
    path('', views.login_view, name="login"),
    path('logout/', views.logoutPage, name='logout'),
    path('forgotpassword/', views.forgotPassword, name='forgotpassword'),
]