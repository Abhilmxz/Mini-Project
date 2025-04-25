from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


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
    path('proof/<int:pk>/', views.view_proof, name='view_proof'),
    path('complaint/edit/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'),
    path('complaint/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),


    


    path('adminover/', views.adminover, name='adminover'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)