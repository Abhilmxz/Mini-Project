from django.urls import path
from . import views


urlpatterns = [
    path("",views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('homelog/', views.homelog, name='homelog'),
    path('profile/', views.profile, name='profile'),

    path('complaint/', views.complaint, name='complaint'),
    path('my_complaints/', views.my_complaints, name='my_complaints'),
    


    path('adminover/', views.adminover, name='adminover'),
]