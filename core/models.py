from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g., Data Analyst at Company X")
    content = CKEditor5Field(config_name='extends', help_text="Testimonial content")
    image = models.ImageField(upload_to='testimonial_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field(config_name='extends', help_text="Event description and details")
    event_date = models.DateTimeField()
    duration = models.CharField(max_length=50, help_text="e.g., 2 hours")
    is_online = models.BooleanField(default=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    registration_deadline = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:event_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = CKEditor5Field(config_name='extends', help_text="Main blog post content")
    excerpt = CKEditor5Field(config_name='default', help_text="Brief excerpt or summary (max 300 characters)")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured_image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class ContactSubmission(models.Model):
    INQUIRY_TYPES = [
        ('general', 'General Inquiry'),
        ('course', 'Course Information'),
        ('admission', 'Admission'),
        ('partnership', 'Partnership'),
        ('career', 'Career Opportunities'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='general')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_responded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class AboutPage(models.Model):
    """Single instance model for About page content"""
    vision = CKEditor5Field(config_name='extends', help_text="Academy's vision statement")
    mission = CKEditor5Field(config_name='extends', help_text="Academy's mission statement")
    values = CKEditor5Field(config_name='extends', help_text="Core values and principles")
    story = CKEditor5Field(config_name='extends', help_text="Journey and credibility of LUM Data Academy")
    partners = CKEditor5Field(config_name='extends', blank=True, help_text="Partners and collaborators information")
    hero_title = models.CharField(max_length=200, default="About LUM Data Academy")
    hero_subtitle = models.CharField(max_length=300, default="Equipping Africa with Future-Ready Data Skills", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Page'

    def __str__(self):
        return "About Page Content"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)


class Career(models.Model):
    """Career opportunities model"""
    title = models.CharField(max_length=200, help_text="Job title")
    slug = models.SlugField(unique=True, blank=True)
    department = models.CharField(max_length=100, help_text="e.g., Academic, Technology, Administration")
    location = models.CharField(max_length=100, help_text="e.g., Nairobi, Remote, Hybrid")
    job_type = models.CharField(max_length=50, choices=[
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ], default='full_time')
    description = CKEditor5Field(config_name='extends', help_text="Detailed job description")
    responsibilities = CKEditor5Field(config_name='extends', help_text="Key responsibilities")
    requirements = CKEditor5Field(config_name='extends', help_text="Required qualifications and skills")
    benefits = CKEditor5Field(config_name='default', blank=True, help_text="Benefits and perks")
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., KShs 50,000 - 80,000")
    application_deadline = models.DateField(null=True, blank=True)
    contact_email = models.EmailField(default='careers@lumdataacademy.org')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text="Show on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Career Opportunity'
        verbose_name_plural = 'Career Opportunities'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:career_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.title} - {self.department}"


class Survey(models.Model):
    """Survey model for collecting feedback"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = CKEditor5Field(config_name='default', help_text="Survey description and purpose")
    content = CKEditor5Field(config_name='extends', help_text="Survey questions and content")
    survey_type = models.CharField(max_length=50, choices=[
        ('course_feedback', 'Course Feedback'),
        ('general_feedback', 'General Feedback'),
        ('market_research', 'Market Research'),
        ('student_satisfaction', 'Student Satisfaction'),
        ('other', 'Other'),
    ], default='general_feedback')
    target_audience = models.CharField(max_length=100, blank=True, help_text="e.g., Students, Alumni, General Public")
    is_active = models.BooleanField(default=True)
    is_anonymous = models.BooleanField(default=True, help_text="Allow anonymous responses")
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    max_responses = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of responses")
    response_count = models.PositiveIntegerField(default=0, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:survey_detail', kwargs={'slug': self.slug})

    def is_open(self):
        """Check if survey is currently open for responses"""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.end_date and now > self.end_date:
            return False
        if self.max_responses and self.response_count >= self.max_responses:
            return False
        return now >= self.start_date

    def __str__(self):
        return self.title