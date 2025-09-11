import random
import uuid
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from .models import MathCaptcha, EmailVerificationToken, PasswordResetToken


def generate_math_captcha(session_key):
    """Generate a math captcha question"""
    # Clear any existing captcha for this session
    MathCaptcha.objects.filter(session_key=session_key).delete()
    
    # Generate random numbers for the math question
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(['+', '-', '*'])
    
    if operation == '+':
        question = f"What is {num1} + {num2}?"
        answer = num1 + num2
    elif operation == '-':
        # Make sure result is positive
        if num1 < num2:
            num1, num2 = num2, num1
        question = f"What is {num1} - {num2}?"
        answer = num1 - num2
    else:  # multiplication
        # Use smaller numbers for multiplication
        num1 = random.randint(2, 10)
        num2 = random.randint(2, 10)
        question = f"What is {num1} × {num2}?"
        answer = num1 * num2
    
    # Create and save the captcha
    captcha = MathCaptcha.objects.create(
        session_key=session_key,
        question=question,
        answer=answer
    )
    
    return captcha


def verify_math_captcha(session_key, user_answer):
    """Verify the math captcha answer"""
    try:
        captcha = MathCaptcha.objects.get(session_key=session_key)
        if captcha.is_expired():
            captcha.delete()
            return False, "Captcha expired. Please try again."
        
        if int(user_answer) == captcha.answer:
            captcha.delete()  # Delete used captcha
            return True, "Correct!"
        else:
            return False, "Incorrect answer. Please try again."
    except (MathCaptcha.DoesNotExist, ValueError):
        return False, "Invalid captcha. Please try again."


def send_verification_email(user, request):
    """Send email verification link"""
    # Delete any existing tokens for this user
    EmailVerificationToken.objects.filter(user=user, is_used=False).delete()
    
    # Create new verification token
    token = EmailVerificationToken.objects.create(
        user=user,
        email=user.email
    )
    
    # Build verification URL
    verification_url = request.build_absolute_uri(
        reverse('accounts:verify_email', kwargs={'token': token.token})
    )
    
    # Email content
    subject = 'Verify Your Email - LUM Data Academy'
    message = f"""
Hello {user.get_full_name() or user.username},

Thank you for registering with LUM Data Academy! Please click the link below to verify your email address:

{verification_url}

This link will expire in 24 hours.

If you didn't create this account, please ignore this email.

Best regards,
LUM Data Academy Team
"""
    
    # Send email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        
        # Update verification sent timestamp
        user.userprofile.email_verification_sent_at = timezone.now()
        user.userprofile.save()
        
        return True, "Verification email sent successfully!"
    except Exception as e:
        return False, f"Failed to send verification email: {str(e)}"


def send_password_reset_email(user, request):
    """Send password reset email"""
    # Delete any existing tokens for this user
    PasswordResetToken.objects.filter(user=user, is_used=False).delete()
    
    # Create new reset token
    token = PasswordResetToken.objects.create(user=user)
    
    # Build reset URL
    reset_url = request.build_absolute_uri(
        reverse('accounts:password_reset_confirm', kwargs={'token': token.token})
    )
    
    # Email content
    subject = 'Password Reset - LUM Data Academy'
    message = f"""
Hello {user.get_full_name() or user.username},

You requested a password reset for your LUM Data Academy account. Click the link below to reset your password:

{reset_url}

This link will expire in 1 hour.

If you didn't request this, please ignore this email. Your password will remain unchanged.

Best regards,
LUM Data Academy Team
"""
    
    # Send email
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        return True, "Password reset email sent successfully!"
    except Exception as e:
        return False, f"Failed to send password reset email: {str(e)}"


def clean_expired_tokens():
    """Clean up expired tokens and captchas"""
    from django.utils import timezone
    
    # Clean expired math captchas
    expired_captchas = MathCaptcha.objects.filter(
        created_at__lt=timezone.now() - timezone.timedelta(minutes=10)
    )
    expired_captchas.delete()
    
    # Clean expired email verification tokens
    expired_email_tokens = EmailVerificationToken.objects.filter(
        created_at__lt=timezone.now() - timezone.timedelta(hours=24)
    )
    expired_email_tokens.delete()
    
    # Clean expired password reset tokens
    expired_password_tokens = PasswordResetToken.objects.filter(
        created_at__lt=timezone.now() - timezone.timedelta(hours=1)
    )
    expired_password_tokens.delete()