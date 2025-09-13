"""
Email services for LUM Data Academy
Comprehensive email system with modern templating and proper error handling
"""
import logging
from typing import Dict, List, Optional, Tuple, Any
from django.conf import settings
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives, send_mail
from django.utils import timezone
from templated_email import send_templated_mail

logger = logging.getLogger(__name__)

class EmailService:
    """
    Centralized email service for LUM Data Academy
    Handles all email operations with proper templating and error handling
    """

    @staticmethod
    def _send_templated_email(
        template_name: str,
        recipient_list: List[str],
        context: Dict[str, Any],
        subject: str,
        from_email: Optional[str] = None,
        fail_silently: bool = False,
        headers: Optional[Dict[str, str]] = None
    ) -> Tuple[bool, str]:
        """
        Send templated email with both HTML and text versions

        Args:
            template_name: Name of the email template (without extension)
            recipient_list: List of recipient email addresses
            context: Template context variables
            subject: Email subject
            from_email: Sender email (defaults to DEFAULT_FROM_EMAIL)
            fail_silently: Whether to suppress exceptions
            headers: Additional email headers

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from_email = from_email or settings.DEFAULT_FROM_EMAIL
            headers = headers or {}

            # Render HTML template
            html_content = render_to_string(f'emails/{template_name}.html', context)

            # Render plain text template
            try:
                text_content = render_to_string(f'emails/{template_name}.txt', context)
            except Exception:
                # If no text template exists, create basic text version
                from html2text import html2text
                text_content = html2text(html_content)

            # Create email message
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=recipient_list,
                headers=headers
            )

            # Attach HTML version
            msg.attach_alternative(html_content, "text/html")

            # Send email
            msg.send(fail_silently=fail_silently)

            logger.info(f"Email '{subject}' sent successfully to {recipient_list}")
            return True, "Email sent successfully"

        except Exception as e:
            error_msg = f"Failed to send email '{subject}': {str(e)}"
            logger.error(error_msg)
            if not fail_silently:
                raise
            return False, error_msg

    @classmethod
    def send_verification_email(cls, user: User, verification_url: str) -> Tuple[bool, str]:
        """
        Send email verification email to user

        Args:
            user: User instance
            verification_url: Verification URL to include in email

        Returns:
            Tuple of (success: bool, message: str)
        """
        context = {
            'user': user,
            'verification_url': verification_url,
            'site_name': 'LUM Data Academy'
        }

        return cls._send_templated_email(
            template_name='verification',
            recipient_list=[user.email],
            context=context,
            subject='Verify Your Email - LUM Data Academy'
        )

    @classmethod
    def send_password_reset_email(cls, user: User, reset_url: str) -> Tuple[bool, str]:
        """
        Send password reset email to user

        Args:
            user: User instance
            reset_url: Password reset URL to include in email

        Returns:
            Tuple of (success: bool, message: str)
        """
        context = {
            'user': user,
            'reset_url': reset_url,
            'site_name': 'LUM Data Academy'
        }

        return cls._send_templated_email(
            template_name='password_reset',
            recipient_list=[user.email],
            context=context,
            subject='Reset Your Password - LUM Data Academy'
        )

    @classmethod
    def send_welcome_email(cls, user: User, login_url: str = None) -> Tuple[bool, str]:
        """
        Send welcome email to new user after email verification

        Args:
            user: User instance
            login_url: Optional login URL

        Returns:
            Tuple of (success: bool, message: str)
        """
        context = {
            'user': user,
            'login_url': login_url or '/accounts/login/',
            'site_name': 'LUM Data Academy'
        }

        return cls._send_templated_email(
            template_name='welcome',
            recipient_list=[user.email],
            context=context,
            subject='Welcome to LUM Data Academy - Your Data Journey Begins!'
        )

    @classmethod
    def send_course_enrollment_email(cls, user: User, course, enrollment_details: Dict = None) -> Tuple[bool, str]:
        """
        Send course enrollment confirmation email

        Args:
            user: User instance
            course: Course instance
            enrollment_details: Additional enrollment information

        Returns:
            Tuple of (success: bool, message: str)
        """
        context = {
            'user': user,
            'course': course,
            'enrollment_details': enrollment_details or {},
            'site_name': 'LUM Data Academy'
        }

        return cls._send_templated_email(
            template_name='course_enrollment',
            recipient_list=[user.email],
            context=context,
            subject=f'Course Enrollment Confirmed - {course.title}'
        )

    @classmethod
    def send_contact_form_response(cls, recipient_email: str, name: str, original_message: str) -> Tuple[bool, str]:
        """
        Send automated response to contact form submissions

        Args:
            recipient_email: Email of person who submitted form
            name: Name of person who submitted form
            original_message: Their original message

        Returns:
            Tuple of (success: bool, message: str)
        """
        context = {
            'name': name,
            'original_message': original_message,
            'site_name': 'LUM Data Academy'
        }

        return cls._send_templated_email(
            template_name='contact_response',
            recipient_list=[recipient_email],
            context=context,
            subject='Thank you for contacting LUM Data Academy'
        )

    @classmethod
    def send_newsletter_subscription_confirmation(cls, email: str, name: str = None) -> Tuple[bool, str]:
        """
        Send newsletter subscription confirmation email

        Args:
            email: Subscriber email
            name: Optional subscriber name

        Returns:
            Tuple of (success: bool, message: str)
        """
        context = {
            'name': name or 'Data Enthusiast',
            'email': email,
            'site_name': 'LUM Data Academy'
        }

        return cls._send_templated_email(
            template_name='newsletter_confirmation',
            recipient_list=[email],
            context=context,
            subject='Welcome to LUM Data Academy Newsletter!'
        )

    @classmethod
    def send_admin_notification(cls, subject: str, message: str, admin_emails: List[str] = None) -> Tuple[bool, str]:
        """
        Send notification email to administrators

        Args:
            subject: Email subject
            message: Email message
            admin_emails: List of admin emails (defaults to settings.ADMINS)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if not admin_emails:
            admin_emails = [email for name, email in getattr(settings, 'ADMINS', [])]
            if not admin_emails:
                admin_emails = ['info@lumdataacademy.org']

        context = {
            'message': message,
            'timestamp': timezone.now(),
            'site_name': 'LUM Data Academy'
        }

        return cls._send_templated_email(
            template_name='admin_notification',
            recipient_list=admin_emails,
            context=context,
            subject=f'[LUM Data Academy] {subject}'
        )

    @staticmethod
    def send_enrollment_confirmation_email(user: User, course, enrollment) -> Tuple[bool, str]:
        """Send enrollment confirmation email with payment instructions"""
        try:
            subject = f'Course Enrollment Confirmed - {course.title} | LUM Data Academy'

            # Build enrollment status URL
            enrollment_status_url = getattr(settings, 'SITE_URL', 'https://lumdataacademy.org')
            enrollment_status_url += f'/courses/enrollment/{enrollment.id}/'

            email_context = {
                'user': user,
                'course': course,
                'enrollment': enrollment,
                'site_name': 'LUM Data Academy',
                'site_url': getattr(settings, 'SITE_URL', 'https://lumdataacademy.org'),
                'enrollment_status_url': enrollment_status_url,
                'current_year': timezone.now().year,
            }

            return EmailService._send_templated_email(
                template_name='enrollment_confirmation',
                recipient_list=[user.email],
                context=email_context,
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL
            )
        except Exception as e:
            logger.error(f"Failed to send enrollment confirmation email to {user.email}: {str(e)}")
            return False, str(e)

    @staticmethod
    def send_course_access_email(user: User, course, enrollment) -> Tuple[bool, str]:
        """Send course access activated email"""
        try:
            subject = f'🎉 Course Access Activated - {course.title} | LUM Data Academy'

            # Build course access URLs
            site_url = getattr(settings, 'SITE_URL', 'https://lumdataacademy.org')
            course_materials_url = f"{site_url}/course/{course.slug}/"
            my_enrollments_url = f"{site_url}/my-enrollments/"

            email_context = {
                'user': user,
                'course': course,
                'enrollment': enrollment,
                'site_name': 'LUM Data Academy',
                'site_url': site_url,
                'course_materials_url': course_materials_url,
                'my_enrollments_url': my_enrollments_url,
                'current_year': timezone.now().year,
            }

            return EmailService._send_templated_email(
                template_name='course_access',
                recipient_list=[user.email],
                context=email_context,
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL
            )
        except Exception as e:
            logger.error(f"Failed to send course access email to {user.email}: {str(e)}")
            return False, str(e)

    @staticmethod
    def send_payment_reminder_email(user: User, enrollment, installment) -> Tuple[bool, str]:
        """Send payment reminder email for installments"""
        try:
            subject = f'Payment Reminder - {enrollment.course.title} | LUM Data Academy'

            # Build enrollment status URL
            enrollment_status_url = getattr(settings, 'SITE_URL', 'https://lumdataacademy.org')
            enrollment_status_url += f'/courses/enrollment/{enrollment.id}/'

            email_context = {
                'user': user,
                'enrollment': enrollment,
                'installment': installment,
                'course': enrollment.course,
                'site_name': 'LUM Data Academy',
                'site_url': getattr(settings, 'SITE_URL', 'https://lumdataacademy.org'),
                'enrollment_status_url': enrollment_status_url,
                'current_year': timezone.now().year,
            }

            return EmailService._send_templated_email(
                template_name='payment_reminder',
                recipient_list=[user.email],
                context=email_context,
                subject=subject,
                from_email=settings.DEFAULT_FROM_EMAIL
            )
        except Exception as e:
            logger.error(f"Failed to send payment reminder email to {user.email}: {str(e)}")
            return False, str(e)


# Legacy compatibility functions for existing code
def send_verification_email(user: User, request) -> Tuple[bool, str]:
    """Legacy function for backward compatibility"""
    from django.urls import reverse
    from accounts.models import EmailVerificationToken

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

    # Use new email service
    success, message = EmailService.send_verification_email(user, verification_url)

    if success:
        # Update verification sent timestamp
        user.userprofile.email_verification_sent_at = timezone.now()
        user.userprofile.save()

    return success, message


def send_password_reset_email(user: User, request) -> Tuple[bool, str]:
    """Legacy function for backward compatibility"""
    from django.urls import reverse
    from accounts.models import PasswordResetToken

    # Delete any existing tokens for this user
    PasswordResetToken.objects.filter(user=user, is_used=False).delete()

    # Create new reset token
    token = PasswordResetToken.objects.create(user=user)

    # Build reset URL
    reset_url = request.build_absolute_uri(
        reverse('accounts:password_reset_confirm', kwargs={'token': token.token})
    )

    # Use new email service
    return EmailService.send_password_reset_email(user, reset_url)