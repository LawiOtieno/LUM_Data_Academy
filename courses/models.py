from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field
import uuid
import string
import random
from django.utils import timezone


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
    # Exchange rates (base currency: USD)
    USD_TO_KES_RATE = 150.0  # 1 USD = 150 KES (approximate)
    USD_TO_NGN_RATE = 800.0  # 1 USD = 800 NGN (approximate)
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
        return reverse('courses:course_detail', kwargs={'slug': self.slug})
    
    def get_display_price(self):
        return self.discount_price if self.discount_price else self.price
    
    def has_discount(self):
        return self.discount_price is not None
    
    def get_savings(self):
        """Calculate the savings amount if there's a discount price"""
        if self.discount_price:
            return self.price - self.discount_price
        return 0
    
    def get_discount_percentage(self):
        """Calculate the discount percentage if there's a discount price"""
        if self.discount_price and self.price > 0:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    def get_price_in_currency(self, currency='KES'):
        """Convert price to specified currency"""
        from decimal import Decimal
        base_price = self.get_display_price()
        
        if currency == 'USD':
            return base_price
        elif currency == 'KES':
            return base_price * Decimal(str(self.USD_TO_KES_RATE))
        elif currency == 'NGN':
            return base_price * Decimal(str(self.USD_TO_NGN_RATE))
        return base_price * Decimal(str(self.USD_TO_KES_RATE))  # Default to KES
    
    def get_original_price_in_currency(self, currency='KES'):
        """Get original price in specified currency"""
        from decimal import Decimal
        if currency == 'USD':
            return self.price
        elif currency == 'KES':
            return self.price * Decimal(str(self.USD_TO_KES_RATE))
        elif currency == 'NGN':
            return self.price * Decimal(str(self.USD_TO_NGN_RATE))
        return self.price * Decimal(str(self.USD_TO_KES_RATE))  # Default to KES
    
    def get_currency_symbol(self, currency='KES'):
        """Get currency symbol"""
        symbols = {
            'USD': '$',
            'KES': 'KShs.',
            'NGN': '₦'
        }
        return symbols.get(currency, 'KShs.')
    
    def get_currency_rate(self, currency='KES'):
        """Get currency conversion rate"""
        if currency == 'KES':
            return self.USD_TO_KES_RATE
        elif currency == 'NGN':
            return self.USD_TO_NGN_RATE
        else:  # USD
            return 1.0
    
    # Template-friendly properties that use default KES currency
    @property
    def price_kes(self):
        """Price in Kenya Shillings"""
        return self.get_price_in_currency('KES')
    
    @property
    def original_price_kes(self):
        """Original price in Kenya Shillings"""
        return self.get_original_price_in_currency('KES')
    
    @property
    def currency_symbol_kes(self):
        """Currency symbol for Kenya Shillings"""
        return self.get_currency_symbol('KES')
    
    @property
    def savings_kes(self):
        """Savings amount in Kenya Shillings"""
        from decimal import Decimal
        if self.discount_price:
            return (self.price - self.discount_price) * Decimal(str(self.USD_TO_KES_RATE))
        return 0
    
    def __str__(self):
        return self.title


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


class Enrollment(models.Model):
    """Course enrollment with payment tracking and activation codes"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Payment Pending'),
        ('partial', 'Partial Payment'),
        ('completed', 'Payment Completed'),
        ('verified', 'Payment Verified'),
    ]
    
    ENROLLMENT_STATUS_CHOICES = [
        ('inactive', 'Inactive'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('suspended', 'Suspended'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
        ('other', 'Other'),
    ]
    
    INSTALLMENT_CHOICES = [
        (1, 'Full Payment'),
        (2, '2 Installments'),
        (3, '3 Installments'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    
    # Payment Information
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='KES')
    installments = models.PositiveIntegerField(choices=INSTALLMENT_CHOICES, default=1)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status and Activation
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    enrollment_status = models.CharField(max_length=20, choices=ENROLLMENT_STATUS_CHOICES, default='inactive')
    activation_code = models.CharField(max_length=19, unique=True, blank=True)  # XXXX-XXXX-XXXX-XXXX format
    is_activated = models.BooleanField(default=False)
    activated_at = models.DateTimeField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    # Admin notes
    admin_notes = models.TextField(blank=True, help_text="Internal notes for administrators")
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'course']
    
    def save(self, *args, **kwargs):
        if not self.activation_code:
            # Generate a unique 16-character activation code
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
            # Format as XXXX-XXXX-XXXX-XXXX
            self.activation_code = '-'.join([code[i:i+4] for i in range(0, 16, 4)])
        super().save(*args, **kwargs)
    
    def activate_enrollment(self):
        """Activate the enrollment"""
        self.is_activated = True
        self.enrollment_status = 'active'
        self.activated_at = timezone.now()
        self.save()
    
    def get_remaining_amount(self):
        """Calculate remaining amount to be paid"""
        return max(0, self.total_amount - self.amount_paid)
    
    def get_payment_progress_percentage(self):
        """Calculate payment progress as percentage"""
        if self.total_amount > 0:
            return min(100, int((self.amount_paid / self.total_amount) * 100))
        return 0
    
    def get_next_installment_amount(self):
        """Get the amount for the next installment"""
        if self.installments == 1:
            return self.total_amount
        
        paid_installments = self.payment_installments.filter(status='verified').count()
        if paid_installments >= self.installments:
            return 0
        
        return self.total_amount / self.installments
    
    def get_payment_instructions(self):
        """Get payment instructions based on payment method"""
        if self.payment_method == 'mpesa':
            return {
                'method': 'M-Pesa',
                'instructions': f'Send KShs {self.get_next_installment_amount():.0f} to: 0768998305\nAccount: LUM ANALYTICA\nInclude your enrollment ID: {self.id} in the message'
            }
        elif self.payment_method == 'paypal':
            return {
                'method': 'PayPal',
                'instructions': f'Send payment to: lum.analytica@gmail.com\nAmount: ${self.get_next_installment_amount():.2f}\nInclude your enrollment ID: {self.id} in the payment note'
            }
        elif self.payment_method == 'bank':
            return {
                'method': 'Bank Transfer',
                'instructions': f'Send payment to: lum.analytica@gmail.com\nAmount: ${self.get_next_installment_amount():.2f}\nInclude your enrollment ID: {self.id} in the payment note'
            }
        return None
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.course.title}"


class PaymentInstallment(models.Model):
    """Individual payment installment tracking"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('verified', 'Verified'),
        ('overdue', 'Overdue'),
    ]
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='payment_installments')
    installment_number = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True, help_text="Payment reference number")
    payment_notes = models.TextField(blank=True, help_text="Additional payment notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['enrollment', 'installment_number']
        unique_together = ['enrollment', 'installment_number']
    
    def is_overdue(self):
        """Check if payment is overdue"""
        from datetime import date
        return self.status == 'pending' and self.due_date < date.today()
    
    def __str__(self):
        return f"{self.enrollment} - Installment {self.installment_number}"