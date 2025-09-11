
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class CourseCategory(models.Model):
    CATEGORY_CHOICES = [
        ('beginner', 'Beginner Courses'),
        ('intermediate', 'Intermediate Courses'),
        ('advanced', 'Advanced Programs'),
        ('masterclass', 'Masterclasses & Short Workshops'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    display_name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Course Categories'
    
    def __str__(self):
        return self.display_name


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='courses')
    overview = models.TextField()
    description = models.TextField()
    duration = models.CharField(max_length=100, help_text="e.g., 8 weeks, 3 months")
    schedule = models.CharField(max_length=100, help_text="e.g., online, evenings")
    learning_outcomes = models.TextField()
    tools_software = models.TextField(help_text="Python, Power BI, R, etc.")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    course_pdf = models.FileField(upload_to='course_pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('core:course_detail', kwargs={'slug': self.slug})
    
    def get_display_price(self):
        return self.discount_price if self.discount_price else self.price
    
    def has_discount(self):
        return self.discount_price is not None
    
    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="e.g., Data Analyst at Company X")
    content = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='testimonials', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.role}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
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
    content = models.TextField()
    excerpt = models.TextField(max_length=300)
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
