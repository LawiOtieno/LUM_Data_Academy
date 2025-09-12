
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.template.response import TemplateResponse
from django.urls import path
from django.contrib.auth.models import User
from .models import Course, BlogPost, Enrollment

class CustomAdminSite(AdminSite):
    site_header = "LUM Data Academy Administration"
    site_title = "LUM Admin"
    index_title = "Welcome to LUM Data Academy Admin Portal"
    
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)
        
        # Sort the apps and models
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        # Custom ordering for our apps
        app_order = ['Core', 'Accounts', 'Authentication and Authorization', 'Emails']
        
        def get_app_priority(app):
            try:
                return app_order.index(app['name'])
            except ValueError:
                return len(app_order)
        
        app_list.sort(key=get_app_priority)
        
        return app_list
    
    def index(self, request, extra_context=None):
        """
        Display the main admin index page.
        """
        app_list = self.get_app_list(request)
        
        # Add statistics to context
        extra_context = extra_context or {}
        try:
            extra_context.update({
                'user_count': User.objects.count(),
                'course_count': Course.objects.count(),
                'blog_count': BlogPost.objects.count(),
                'enrollment_count': Enrollment.objects.count(),
            })
        except:
            extra_context.update({
                'user_count': 0,
                'course_count': 0,
                'blog_count': 0,
                'enrollment_count': 0,
            })
        
        extra_context.update({
            'title': self.index_title,
            'app_list': app_list,
            'has_permission': self.has_permission(request),
        })
        
        return TemplateResponse(request, 'admin/index.html', extra_context)

# Create custom admin site instance
custom_admin_site = CustomAdminSite(name='custom_admin')
