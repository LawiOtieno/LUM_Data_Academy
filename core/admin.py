from django.contrib import admin
from django.db import models
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import (
    CourseCategory, Course, CourseModule, CodeExample, 
    Exercise, CapstoneProject, Testimonial, Event, 
    BlogPost, ContactSubmission, Newsletter, AboutPage,
    Enrollment, PaymentInstallment
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


# Enrollment system admin classes
class PaymentInstallmentInline(admin.TabularInline):
    model = PaymentInstallment
    extra = 0
    fields = ('installment_number', 'amount', 'due_date', 'status', 'payment_date', 'payment_reference')
    readonly_fields = ('installment_number', 'amount', 'due_date')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'payment_status', 'is_activated', 'payment_method', 'installments', 'amount_paid', 'created_at')
    list_filter = ('payment_status', 'is_activated', 'payment_method', 'installments', 'created_at')
    search_fields = ('user__username', 'user__email', 'course__title', 'activation_code')
    readonly_fields = ('activation_code', 'created_at', 'updated_at', 'activated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Enrollment Information', {
            'fields': ('user', 'course', 'activation_code', 'is_activated', 'activated_at')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'currency', 'total_amount', 'amount_paid', 
                      'payment_status', 'installments')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [PaymentInstallmentInline]
    
    def save_model(self, request, obj, form, change):
        # Auto-generate activation code if not present
        if not obj.activation_code:
            import uuid
            obj.activation_code = str(uuid.uuid4()).replace('-', '').upper()[:16]
            # Format as XXXX-XXXX-XXXX-XXXX
            obj.activation_code = '-'.join([
                obj.activation_code[i:i+4] for i in range(0, 16, 4)
            ])
        super().save_model(request, obj, form, change)
    
    actions = ['activate_enrollment', 'mark_payment_complete', 'send_activation_email']
    
    def activate_enrollment(self, request, queryset):
        """Custom admin action to activate enrollments"""
        from django.utils import timezone
        updated = 0
        for enrollment in queryset.filter(payment_status='completed', is_activated=False):
            enrollment.is_activated = True
            enrollment.activated_at = timezone.now()
            enrollment.save()
            updated += 1
            
            # Send course access email
            try:
                from emails.services import EmailService
                EmailService.send_course_access_email(enrollment.user, enrollment.course, enrollment)
            except Exception as e:
                pass  # Continue even if email fails
                
        self.message_user(request, f'Successfully activated {updated} enrollments.')
    activate_enrollment.short_description = "Activate selected enrollments"
    
    def mark_payment_complete(self, request, queryset):
        """Mark payments as complete"""
        updated = queryset.filter(payment_status__in=['pending', 'partial']).update(
            payment_status='completed',
            amount_paid=models.F('total_amount')
        )
        self.message_user(request, f'Marked {updated} payments as complete.')
    mark_payment_complete.short_description = "Mark payments as complete"
    
    def send_activation_email(self, request, queryset):
        """Send activation emails to students"""
        sent = 0
        for enrollment in queryset:
            try:
                from emails.services import EmailService
                if enrollment.payment_status == 'completed' and not enrollment.is_activated:
                    # Send activation email with code
                    EmailService.send_course_access_email(enrollment.user, enrollment.course, enrollment)
                else:
                    # Send enrollment confirmation with payment instructions
                    EmailService.send_enrollment_confirmation_email(enrollment.user, enrollment.course, enrollment)
                sent += 1
            except Exception as e:
                pass  # Continue even if email fails
        self.message_user(request, f'Sent activation emails to {sent} students.')
    send_activation_email.short_description = "Send activation emails"


@admin.register(PaymentInstallment)
class PaymentInstallmentAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'installment_number', 'amount', 'due_date', 'status', 'payment_date', 'payment_reference')
    list_filter = ('status', 'due_date', 'payment_date', 'created_at')
    search_fields = ('enrollment__user__username', 'enrollment__course__title', 'payment_reference')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('enrollment', 'installment_number')
    
    fieldsets = (
        ('Installment Information', {
            'fields': ('enrollment', 'installment_number', 'amount', 'due_date')
        }),
        ('Payment Status', {
            'fields': ('status', 'payment_date', 'payment_reference', 'payment_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('enrollment__user', 'enrollment__course')
    
    actions = ['mark_as_paid', 'mark_as_verified', 'send_reminder_email']
    
    def mark_as_paid(self, request, queryset):
        """Mark installments as paid"""
        from django.utils import timezone
        updated = 0
        for installment in queryset.filter(status='pending'):
            installment.status = 'paid'
            installment.payment_date = timezone.now()
            installment.save()
            updated += 1
        self.message_user(request, f'Marked {updated} installments as paid.')
    mark_as_paid.short_description = "Mark as paid"
    
    def mark_as_verified(self, request, queryset):
        """Mark installments as verified"""
        from django.utils import timezone
        updated = 0
        for installment in queryset.filter(status='paid'):
            installment.status = 'verified'
            installment.save()
            
            # Update enrollment paid amount
            enrollment = installment.enrollment
            enrollment.amount_paid += installment.amount
            if enrollment.amount_paid >= enrollment.total_amount:
                enrollment.payment_status = 'completed'
            else:
                enrollment.payment_status = 'partial'
            enrollment.save()
            updated += 1
            
        self.message_user(request, f'Verified {updated} installments.')
    mark_as_verified.short_description = "Mark as verified"
    
    def send_reminder_email(self, request, queryset):
        """Send payment reminder emails"""
        sent = 0
        for installment in queryset.filter(status='pending'):
            try:
                from emails.services import EmailService
                EmailService.send_payment_reminder_email(
                    installment.enrollment.user, 
                    installment.enrollment, 
                    installment
                )
                sent += 1
            except Exception as e:
                pass  # Continue even if email fails
        self.message_user(request, f'Sent reminder emails for {sent} installments.')
    send_reminder_email.short_description = "Send payment reminders"