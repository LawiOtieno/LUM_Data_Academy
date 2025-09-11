
from django.contrib import admin
from .models import CourseCategory, Course, Testimonial, Event, BlogPost, ContactSubmission, Newsletter


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'discount_price', 'is_featured', 'is_active', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active', 'created_at')
    search_fields = ('title', 'overview', 'description')
    list_editable = ('is_featured', 'is_active')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'course', 'is_featured', 'created_at')
    list_filter = ('is_featured', 'course', 'created_at')
    search_fields = ('name', 'role', 'content')
    list_editable = ('is_featured',)
    ordering = ('-created_at',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'price', 'is_online', 'is_active', 'created_at')
    list_filter = ('is_online', 'is_active', 'event_date', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_active',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('event_date',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at', 'updated_at')
    list_filter = ('is_published', 'author', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('-created_at',)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'inquiry_type', 'subject', 'is_responded', 'created_at')
    list_filter = ('inquiry_type', 'is_responded', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_responded',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'subscribed_at', 'is_active')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    list_editable = ('is_active',)
    readonly_fields = ('subscribed_at',)
    ordering = ('-subscribed_at',)
