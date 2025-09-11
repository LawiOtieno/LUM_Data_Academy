from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    CourseCategory, Course, CourseModule, CodeExample, 
    Exercise, CapstoneProject, Testimonial, Event, 
    BlogPost, ContactSubmission, Newsletter, AboutPage
)


class CourseModuleInline(admin.TabularInline):
    model = CourseModule
    extra = 1
    fields = ('title', 'order', 'duration_hours', 'video_url', 'is_active')
    show_change_link = True


class CodeExampleInline(admin.TabularInline):
    model = CodeExample
    extra = 1
    fields = ('title', 'language', 'difficulty_level', 'order', 'is_interactive')
    show_change_link = True


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1
    fields = ('title', 'difficulty_level', 'estimated_time_minutes', 'order', 'is_graded', 'points')
    show_change_link = True


class CapstoneProjectInline(admin.TabularInline):
    model = CapstoneProject
    extra = 1
    fields = ('title', 'difficulty_level', 'estimated_hours', 'order', 'is_group_project')
    show_change_link = True


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'order')
    list_editable = ('order',)
    ordering = ('order',)
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='default')}
    }


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discount_price', 'total_modules', 'estimated_hours', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'overview', 'tools_software')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'overview', 'description')
        }),
        ('Course Details', {
            'fields': ('duration', 'schedule', 'learning_outcomes', 'tools_software', 
                      'prerequisites', 'course_syllabus')
        }),
        ('Pricing & Media', {
            'fields': ('price', 'discount_price', 'image', 'video_intro_url', 'course_pdf')
        }),
        ('Course Structure', {
            'fields': ('total_modules', 'estimated_hours')
        }),
        ('Status & Visibility', {
            'fields': ('is_featured', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [CourseModuleInline, CapstoneProjectInline]
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        # Update total modules count after inline formsets are saved
        form.instance.total_modules = form.instance.modules.count()
        form.instance.save(update_fields=['total_modules'])


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'duration_hours', 'is_active', 'created_at')
    list_filter = ('course', 'is_active', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    list_editable = ('order', 'is_active')
    ordering = ('course', 'order')
    
    fieldsets = (
        ('Module Information', {
            'fields': ('course', 'title', 'description', 'content', 'order')
        }),
        ('Learning Details', {
            'fields': ('learning_objectives', 'duration_hours', 'video_url')
        }),
        ('Resources & Status', {
            'fields': ('resources', 'is_active')
        }),
    )
    
    inlines = [CodeExampleInline, ExerciseInline]
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(CodeExample)
class CodeExampleAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'language', 'difficulty_level', 'order', 'is_interactive')
    list_filter = ('language', 'difficulty_level', 'is_interactive', 'created_at')
    search_fields = ('title', 'description', 'code', 'module__title')
    list_editable = ('order', 'is_interactive')
    ordering = ('module', 'order')
    
    fieldsets = (
        ('Example Information', {
            'fields': ('module', 'title', 'description', 'language', 'difficulty_level', 'order')
        }),
        ('Code Content', {
            'fields': ('code', 'explanation', 'expected_output')
        }),
        ('Interactive Features', {
            'fields': ('is_interactive',)
        }),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'difficulty_level', 'estimated_time_minutes', 'order', 'is_graded', 'points')
    list_filter = ('difficulty_level', 'is_graded', 'created_at')
    search_fields = ('title', 'description', 'module__title')
    list_editable = ('order', 'is_graded', 'points')
    ordering = ('module', 'order')
    
    fieldsets = (
        ('Exercise Information', {
            'fields': ('module', 'title', 'description', 'difficulty_level', 'order')
        }),
        ('Completion Details', {
            'fields': ('estimated_time_minutes', 'hints', 'solution', 'dataset_url')
        }),
        ('Grading', {
            'fields': ('is_graded', 'points')
        }),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(CapstoneProject)
class CapstoneProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'difficulty_level', 'estimated_hours', 'order', 'is_group_project')
    list_filter = ('difficulty_level', 'is_group_project', 'created_at')
    search_fields = ('title', 'description', 'course__title')
    list_editable = ('order', 'is_group_project')
    ordering = ('course', 'order')
    
    fieldsets = (
        ('Project Information', {
            'fields': ('course', 'title', 'description', 'requirements', 'order')
        }),
        ('Project Details', {
            'fields': ('evaluation_criteria', 'estimated_hours', 'difficulty_level')
        }),
        ('Resources & Data', {
            'fields': ('sample_datasets', 'deliverables', 'resources')
        }),
        ('Group Settings', {
            'fields': ('is_group_project', 'max_group_size')
        }),
    )
    
    formfield_overrides = {
        models.TextField: {'widget': CKEditor5Widget(config_name='extends')}
    }


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'course', 'is_featured', 'created_at')
    list_filter = ('course', 'is_featured', 'created_at')
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