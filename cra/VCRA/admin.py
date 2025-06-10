from django.contrib import admin
from .models import UserRegistration
from .models import Feedback


from django.urls import path
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile_number', 'date_of_birth', 'created_at')  # Now includes 'created_at'
    search_fields = ('full_name', 'email', 'mobile_number')
    list_filter = ('date_of_birth',)
    ordering = ('created_at',)  # Ordering by 'created_at'
    readonly_fields = ('email',)  # Read-only fields for editing


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='admin-dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        return TemplateResponse(request, "adminover.html", {})

admin_site = CustomAdminSite(name='custom_admin')



@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'message', 'created_at')
    

