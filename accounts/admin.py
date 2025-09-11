from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, MathCaptcha, EmailVerificationToken, PasswordResetToken


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Information'
    fields = ('role', 'phone_number', 'bio', 'profile_image', 'date_of_birth', 
              'location', 'linkedin_profile', 'github_profile', 'website', 
              'is_email_verified', 'profile_completed')


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 
                    'is_email_verified', 'is_staff', 'date_joined')
    list_filter = ('userprofile__role', 'userprofile__is_email_verified', 
                   'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    def get_role(self, obj):
        return obj.userprofile.get_role_display() if hasattr(obj, 'userprofile') else 'No Profile'
    get_role.short_description = 'Role'
    
    def is_email_verified(self, obj):
        return obj.userprofile.is_email_verified if hasattr(obj, 'userprofile') else False
    is_email_verified.boolean = True
    is_email_verified.short_description = 'Email Verified'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone_number', 'location', 'is_email_verified', 
                    'profile_completed', 'created_at')
    list_filter = ('role', 'is_email_verified', 'profile_completed', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 
                     'user__last_name', 'phone_number', 'location')
    readonly_fields = ('email_verification_token', 'created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'role')
        }),
        ('Personal Information', {
            'fields': ('phone_number', 'bio', 'profile_image', 'date_of_birth', 'location')
        }),
        ('Social Links', {
            'fields': ('linkedin_profile', 'github_profile', 'website'),
            'classes': ('collapse',)
        }),
        ('Account Status', {
            'fields': ('is_email_verified', 'email_verification_token', 
                       'email_verification_sent_at', 'profile_completed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(MathCaptcha)
class MathCaptchaAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'session_key', 'created_at', 'is_expired')
    list_filter = ('created_at',)
    search_fields = ('session_key', 'question')
    readonly_fields = ('created_at',)
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


@admin.register(EmailVerificationToken)
class EmailVerificationTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'token', 'created_at', 'is_used', 'is_expired')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email', 'email', 'token')
    readonly_fields = ('token', 'created_at')
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at', 'is_used', 'is_expired')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email', 'token')
    readonly_fields = ('token', 'created_at')
    
    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True
    is_expired.short_description = 'Expired'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
