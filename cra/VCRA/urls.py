from django.urls import path
from . import views


urlpatterns = [
    path("",views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('homelog/', views.homelog, name='homelog'),
    path('profile/', views.profile, name='profile'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
]