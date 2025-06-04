from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    # Public/User Views
    path("", views.home, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('login/', views.user_login, name='user_login'),       # For user login (email/password)
    path('admin-login/', views.admin_login, name='admin_login'),  # For admin login (username/password)
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    path('homelog/', views.homelog, name='homelog'),
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),
    path('form/', views.civic_form_view, name='civic_form'),
    path('form/success/', views.success_view, name='success'),
    

    # Complaint Submission (User)
    path('complaint/', views.complaint, name='complaint'),
    path('submit-feedback/', views.submit_feedback, name='submit_feedback'),
    path('my_complaints/', views.my_complaints, name='my_complaints'),
    path('proof/<int:pk>/', views.view_proof, name='view_proof'),
    path('complaint/edit/<int:complaint_id>/', views.edit_complaint, name='edit_complaint'),
    path('complaint/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),

    # Admin Views
    path('adminover/', views.adminover, name='adminover'),
    path('adminpanel/user/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('adminpanel/users/', views.user_list, name='user_list'),  # This line is critical
    path('adminpanel/user/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    path('admin_comp/', views.admin_complaints_view, name='admin_comp'),
    path('complaint/<int:pk>/status/<str:status>/', views.update_complaint_status, name='update_complaint_status'),
    path('admin/complaints/<int:pk>/edit/', views.edit_admin_complaint, name='admin_edit_complaint'),

    # Admin: User Management & Feedback
    path('user_manage/', views.user_manage, name='user_manage'),
    path('admin/feedback/', views.feedback_admin_view, name='feedback_admin'),
    path('feedback/', views.feedback_view, name='feedback'),
]

# Serve uploaded files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
