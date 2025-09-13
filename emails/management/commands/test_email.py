
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from emails.services import EmailService


class Command(BaseCommand):
    help = 'Test the email system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--email',
            type=str,
            default='test@example.com',
            help='Email address to send test to'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['welcome', 'contact', 'newsletter', 'admin'],
            default='welcome',
            help='Type of email to test'
        )

    def handle(self, *args, **options):
        email = options['email']
        email_type = options['type']
        
        self.stdout.write(f'Testing {email_type} email to {email}...')
        
        try:
            # Get or create a test user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            
            if email_type == 'welcome':
                success, message = EmailService.send_welcome_email(user)
            elif email_type == 'contact':
                success, message = EmailService.send_contact_form_response(
                    email, 'Test User', 'This is a test message.'
                )
            elif email_type == 'newsletter':
                success, message = EmailService.send_newsletter_subscription_confirmation(
                    email, 'Test User'
                )
            elif email_type == 'admin':
                success, message = EmailService.send_admin_notification(
                    'Test Notification',
                    'This is a test admin notification.',
                    [email]
                )
            
            if success:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Email sent successfully!')
                )
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Failed to send email: {message}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {str(e)}')
            )
