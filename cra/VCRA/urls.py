from django.urls import path
from . import views


urlpatterns = [
    path("",views.home),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('homelog/', views.homelog, name='homelog'),
]