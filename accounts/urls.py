from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Email verification
    path('verify-email/<uuid:token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    
    # Password reset
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset-confirm/<uuid:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    
    # Dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('learner-dashboard/', views.learner_dashboard, name='learner_dashboard'),
    path('instructor-dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    
    # Profile management
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    
    # AJAX endpoints
    path('generate-captcha/', views.generate_captcha_ajax, name='generate_captcha'),
]