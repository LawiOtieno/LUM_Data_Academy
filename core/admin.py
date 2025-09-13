from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    Testimonial, Event, BlogPost, ContactSubmission, 
    Newsletter, AboutPage, Career, Survey
)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'created_at')
    search_fields = ('name', 'role', 'content')
    list_editable = ('is_featured',)
    ordering = ('-created_at',)
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')}
    }


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'duration', 'is_online', 'price', 'is_active')
    list_filter = ('is_online', 'is_active', 'event_date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('event_date',)
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    list_filter = ('is_published', 'author', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'created_at', 'is_responded')
    list_filter = ('inquiry_type', 'is_responded', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_responded',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')}
    }


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    list_editable = ('is_active',)
    readonly_fields = ('subscribed_at',)
    ordering = ('-subscribed_at',)


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance
        return not AboutPage.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion of the single instance
        return False
    
    fieldsets = (
        ('Page Hero', {
            'fields': ('hero_title', 'hero_subtitle')
        }),
        ('Vision & Mission', {
            'fields': ('vision', 'mission', 'values')
        }),
        ('Academy Story', {
            'fields': ('story',)
        }),
        ('Partners & Collaborators', {
            'fields': ('partners',)
        }),
        ('Last Updated', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('updated_at',)
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'location', 'job_type', 'is_active', 'is_featured', 'application_deadline', 'created_at')
    list_filter = ('department', 'job_type', 'location', 'is_active', 'is_featured', 'created_at')
    search_fields = ('title', 'department', 'description', 'requirements')
    list_editable = ('is_active', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'department', 'location', 'job_type')
        }),
        ('Job Details', {
            'fields': ('description', 'responsibilities', 'requirements', 'benefits')
        }),
        ('Application Info', {
            'fields': ('salary_range', 'application_deadline', 'contact_email')
        }),
        ('Visibility', {
            'fields': ('is_active', 'is_featured')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'survey_type', 'target_audience', 'is_active', 'is_anonymous', 'response_count', 'start_date', 'end_date')
    list_filter = ('survey_type', 'is_active', 'is_anonymous', 'start_date', 'created_at')
    search_fields = ('title', 'description', 'target_audience')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('response_count', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Survey Information', {
            'fields': ('title', 'slug', 'description', 'content', 'survey_type')
        }),
        ('Settings', {
            'fields': ('target_audience', 'is_active', 'is_anonymous', 'max_responses')
        }),
        ('Schedule', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('response_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Only set created_by for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }