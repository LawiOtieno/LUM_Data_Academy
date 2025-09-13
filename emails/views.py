
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.conf import settings
from .services import EmailService
import logging

logger = logging.getLogger(__name__)

@staff_member_required
def test_email_system(request):
    """Test the email system with various email types"""
    if request.method == 'POST':
        email_type = request.POST.get('email_type')
        test_email = request.POST.get('test_email', 'test@example.com')
        
        try:
            if email_type == 'welcome':
                success, message = EmailService.send_welcome_email(
                    request.user, 
                    login_url='https://lumdataacademy.org/accounts/login/'
                )
            elif email_type == 'contact_response':
                success, message = EmailService.send_contact_form_response(
                    test_email,
                    'Test User',
                    'This is a test message to verify the email system is working.'
                )
            elif email_type == 'newsletter':
                success, message = EmailService.send_newsletter_subscription_confirmation(
                    test_email,
                    'Test User'
                )
            elif email_type == 'admin_notification':
                success, message = EmailService.send_admin_notification(
                    'Email System Test',
                    'This is a test notification to verify the admin email system is working.',
                    [test_email]
                )
            else:
                success, message = False, 'Invalid email type'
            
            if success:
                messages.success(request, f'✅ {email_type.title()} email sent successfully!')
            else:
                messages.error(request, f'❌ Failed to send {email_type} email: {message}')
                
        except Exception as e:
            logger.error(f"Email test failed: {str(e)}")
            messages.error(request, f'❌ Email test failed: {str(e)}')
        
        return redirect('admin:test_email_system')
    
    # Check email configuration
    email_config = {
        'EMAIL_BACKEND': getattr(settings, 'EMAIL_BACKEND', 'Not configured'),
        'EMAIL_HOST': getattr(settings, 'EMAIL_HOST', 'Not configured'),
        'EMAIL_PORT': getattr(settings, 'EMAIL_PORT', 'Not configured'),
        'EMAIL_USE_TLS': getattr(settings, 'EMAIL_USE_TLS', 'Not configured'),
        'DEFAULT_FROM_EMAIL': getattr(settings, 'DEFAULT_FROM_EMAIL', 'Not configured'),
    }
    
    context = {
        'email_config': email_config,
        'title': 'Email System Test',
    }
    
    return render(request, 'emails/test_system.html', context)
