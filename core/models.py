
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


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
    overview = CKEditor5Field(config_name='default', help_text="Brief course overview")
    description = CKEditor5Field(config_name='extends', help_text="Detailed course description")
    duration = models.CharField(max_length=100, help_text="e.g., 8 weeks, 3 months")
    schedule = models.CharField(max_length=100, help_text="e.g., online, evenings")
    learning_outcomes = CKEditor5Field(config_name='default', help_text="What students will learn")
    tools_software = models.TextField(help_text="Python, Power BI, R, etc.")
    prerequisites = CKEditor5Field(config_name='default', blank=True, help_text="Course prerequisites")
    course_syllabus = CKEditor5Field(config_name='extends', blank=True, help_text="Detailed course syllabus")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    course_pdf = models.FileField(upload_to='course_pdfs/', blank=True, null=True)
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    video_intro_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL for course intro")
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    total_modules = models.PositiveIntegerField(default=0, help_text="Total number of modules")
    estimated_hours = models.PositiveIntegerField(default=0, help_text="Estimated completion time in hours")
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


class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='default', help_text="Module overview")
    content = CKEditor5Field(config_name='extends', help_text="Detailed module content")
    order = models.PositiveIntegerField(default=0)
    duration_hours = models.PositiveIntegerField(default=0, help_text="Estimated hours to complete")
    video_url = models.URLField(blank=True, help_text="YouTube or Vimeo URL for module video")
    learning_objectives = CKEditor5Field(config_name='default', blank=True, help_text="What students will learn in this module")
    resources = CKEditor5Field(config_name='default', blank=True, help_text="Additional resources and reading materials")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - Module {self.order}: {self.title}"
    
    def get_exercises_count(self):
        return self.exercises.count()
    
    def get_code_examples_count(self):
        return self.code_examples.count()


class CodeExample(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='code_examples')
    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='default', help_text="Explanation of the code example")
    code = models.TextField(help_text="The actual code")
    language = models.CharField(max_length=50, default='python', help_text="Programming language (python, r, sql, etc.)")
    explanation = CKEditor5Field(config_name='extends', help_text="Detailed explanation of the code")
    expected_output = models.TextField(blank=True, help_text="Expected output when code is run")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')
    order = models.PositiveIntegerField(default=0)
    is_interactive = models.BooleanField(default=False, help_text="Can students run this code?")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.module.title} - {self.title}"


class Exercise(models.Model):
    module = models.ForeignKey(CourseModule, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='extends', help_text="Exercise instructions and requirements")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='beginner')
    estimated_time_minutes = models.PositiveIntegerField(default=30, help_text="Estimated completion time in minutes")
    hints = CKEditor5Field(config_name='default', blank=True, help_text="Helpful hints for students")
    solution = CKEditor5Field(config_name='extends', blank=True, help_text="Sample solution (optional)")
    dataset_url = models.URLField(blank=True, help_text="URL to download exercise dataset")
    order = models.PositiveIntegerField(default=0)
    is_graded = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0, help_text="Points awarded for completion")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.module.title} - Exercise: {self.title}"


class CapstoneProject(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='capstone_projects')
    title = models.CharField(max_length=200)
    description = CKEditor5Field(config_name='extends', help_text="Detailed project requirements and objectives")
    requirements = CKEditor5Field(config_name='extends', help_text="Technical requirements and deliverables")
    evaluation_criteria = CKEditor5Field(config_name='default', help_text="How the project will be evaluated")
    estimated_hours = models.PositiveIntegerField(default=40, help_text="Estimated completion time in hours")
    difficulty_level = models.CharField(max_length=20, choices=[
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced')
    ], default='intermediate')
    sample_datasets = CKEditor5Field(config_name='default', blank=True, help_text="Information about datasets to be used")
    deliverables = CKEditor5Field(config_name='default', help_text="What students need to submit")
    resources = CKEditor5Field(config_name='default', blank=True, help_text="Additional resources and references")
    order = models.PositiveIntegerField(default=0)
    is_group_project = models.BooleanField(default=False, help_text="Is this a group project?")
    max_group_size = models.PositiveIntegerField(default=1, help_text="Maximum group size if group project")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['course', 'order']
    
    def __str__(self):
        return f"{self.course.title} - Capstone: {self.title}"
