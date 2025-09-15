
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib.admin import AdminSite
from django.utils.html import format_html
from . import views

class EmailsAdminConfig:
    """Custom admin configuration for emails app"""
    
    def get_urls(self):
        """Add custom admin URLs"""
        urls = super().get_urls() if hasattr(super(), 'get_urls') else []
        custom_urls = [
            path('test-email-system/', views.test_email_system, name='test_email_system'),
        ]
        return custom_urls + urls

# Add custom admin action
def test_email_system_action(modeladmin, request, queryset):
    """Redirect to email test system"""
    return redirect('/emails/test/')

test_email_system_action.short_description = "🧪 Test Email System"
