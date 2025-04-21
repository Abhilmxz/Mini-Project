from django.contrib import admin
from .models import UserRegistration

@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'mobile_number', 'date_of_birth', 'created_at')  # Now includes 'created_at'
    search_fields = ('full_name', 'email', 'mobile_number')
    list_filter = ('date_of_birth',)
    ordering = ('created_at',)  # Ordering by 'created_at'
    readonly_fields = ('email',)  # Read-only fields for editing