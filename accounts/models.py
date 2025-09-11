from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('learner', 'Learner'),
        ('instructor', 'Instructor'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='learner')
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin_profile = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    website = models.URLField(blank=True)
    
    # Account status
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    email_verification_sent_at = models.DateTimeField(blank=True, null=True)
    
    # Profile completion
    profile_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.get_role_display()}"
    
    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username
    
    @property
    def is_instructor(self):
        return self.role == 'instructor'
    
    @property
    def is_learner(self):
        return self.role == 'learner'
    
    def get_profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        total_fields = 8
        completed_fields = 0
        
        if self.user.first_name and self.user.last_name:
            completed_fields += 1
        if self.phone_number:
            completed_fields += 1
        if self.bio:
            completed_fields += 1
        if self.profile_image:
            completed_fields += 1
        if self.date_of_birth:
            completed_fields += 1
        if self.location:
            completed_fields += 1
        if self.linkedin_profile or self.github_profile or self.website:
            completed_fields += 1
        if self.is_email_verified:
            completed_fields += 1
            
        return int((completed_fields / total_fields) * 100)


class MathCaptcha(models.Model):
    """Math captcha for registration verification"""
    session_key = models.CharField(max_length=255, unique=True)
    question = models.CharField(max_length=100)
    answer = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Math Captcha: {self.question}"
    
    def is_expired(self):
        """Check if captcha is older than 10 minutes"""
        return timezone.now() > self.created_at + timezone.timedelta(minutes=10)


class EmailVerificationToken(models.Model):
    """Email verification tokens for secure email verification"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Email verification for {self.user.username}"
    
    def is_expired(self):
        """Check if token is older than 24 hours"""
        return timezone.now() > self.created_at + timezone.timedelta(hours=24)


class PasswordResetToken(models.Model):
    """Password reset tokens"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Password reset for {self.user.username}"
    
    def is_expired(self):
        """Check if token is older than 1 hour"""
        return timezone.now() > self.created_at + timezone.timedelta(hours=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a user profile when a user is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile when user is saved"""
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
