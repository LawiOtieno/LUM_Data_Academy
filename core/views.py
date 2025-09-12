
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetime import timedelta, date
import json

from .models import Course, CourseCategory, Testimonial, Event, BlogPost, ContactSubmission, Newsletter, AboutPage, Enrollment, PaymentInstallment
from .forms import ContactForm, NewsletterForm


def home(request):
    """Modern homepage with dynamic content"""
    featured_courses = Course.objects.filter(is_featured=True, is_active=True)[:3]
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]
    upcoming_events = Event.objects.filter(is_active=True).order_by('event_date')[:3]
    recent_blogs = BlogPost.objects.filter(is_published=True)[:3]
    
    context = {
        'featured_courses': featured_courses,
        'testimonials': testimonials,
        'upcoming_events': upcoming_events,
        'recent_blogs': recent_blogs,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About us page"""
    try:
        about_page = AboutPage.objects.get(pk=1)
    except AboutPage.DoesNotExist:
        # Create default instance if it doesn't exist
        about_page = AboutPage.objects.create(
            hero_title="About LUM Data Academy",
            hero_subtitle="Equipping Africa with Future-Ready Data Skills",
            vision="Our vision is to equip Africa with future-ready data skills.",
            mission="To bridge the data skills gap across Africa through world-class training programs.",
            values="Excellence, Innovation, Accessibility, Impact",
            story="Founded with the vision of transforming careers through practical, industry-relevant education."
        )
    
    return render(request, 'core/about.html', {'about': about_page})


def courses(request):
    """Courses listing with modern filtering"""
    categories = CourseCategory.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    selected_currency = request.GET.get('currency', 'KES')
    
    courses_list = Course.objects.filter(is_active=True)
    
    if category_slug:
        courses_list = courses_list.filter(category__name=category_slug)
    
    if search_query:
        courses_list = courses_list.filter(title__icontains=search_query)
    
    paginator = Paginator(courses_list, 9)
    page_number = request.GET.get('page')
    courses_page = paginator.get_page(page_number)
    
    currencies = [
        {'code': 'KES', 'name': 'Kenyan Shillings', 'symbol': 'KShs.'},
        {'code': 'USD', 'name': 'US Dollars', 'symbol': '$'},
        {'code': 'NGN', 'name': 'Nigerian Nairas', 'symbol': '₦'},
    ]
    
    context = {
        'courses': courses_page,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
        'currencies': currencies,
        'selected_currency': selected_currency,
    }
    return render(request, 'core/courses.html', context)


def course_detail(request, slug):
    """Individual course detail page with enrollment status"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    related_courses = Course.objects.filter(
        category=course.category, 
        is_active=True
    ).exclude(id=course.id)[:3]
    
    selected_currency = request.GET.get('currency', 'KES')
    currencies = [
        {'code': 'KES', 'name': 'Kenyan Shillings', 'symbol': 'KShs.'},
        {'code': 'USD', 'name': 'US Dollars', 'symbol': '$'},
        {'code': 'NGN', 'name': 'Nigerian Nairas', 'symbol': '₦'},
    ]
    
    # Check enrollment status for authenticated users
    user_enrollment = None
    if request.user.is_authenticated:
        try:
            user_enrollment = Enrollment.objects.get(user=request.user, course=course)
        except Enrollment.DoesNotExist:
            pass
    
    context = {
        'course': course,
        'related_courses': related_courses,
        'currencies': currencies,
        'selected_currency': selected_currency,
        'user_enrollment': user_enrollment,
    }
    return render(request, 'core/course_detail.html', context)


def events(request):
    """Events listing"""
    events_list = Event.objects.filter(is_active=True).order_by('event_date')
    
    paginator = Paginator(events_list, 6)
    page_number = request.GET.get('page')
    events_page = paginator.get_page(page_number)
    
    context = {
        'events': events_page,
    }
    return render(request, 'core/events.html', context)


def event_detail(request, slug):
    """Individual event detail page"""
    event = get_object_or_404(Event, slug=slug, is_active=True)
    return render(request, 'core/event_detail.html', {'event': event})


def blog(request):
    """Blog listing"""
    posts_list = BlogPost.objects.filter(is_published=True)
    
    paginator = Paginator(posts_list, 6)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    context = {
        'posts': posts_page,
    }
    return render(request, 'core/blog.html', context)


def blog_detail(request, slug):
    """Individual blog post"""
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'recent_posts': recent_posts,
    }
    return render(request, 'core/blog_detail.html', context)


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you! Your message has been sent. We\'ll get back to you soon!')
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})


@require_http_methods(["POST"])
def newsletter_subscribe(request):
    """AJAX newsletter subscription"""
    try:
        data = json.loads(request.body)
        email = data.get('email')
        name = data.get('name', '')
        
        if not email:
            return JsonResponse({'success': False, 'message': 'Email is required'})
        
        newsletter, created = Newsletter.objects.get_or_create(
            email=email,
            defaults={'name': name}
        )
        
        if created:
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to our newsletter!'})
        else:
            return JsonResponse({'success': False, 'message': 'You are already subscribed!'})
            
    except Exception as e:
        return JsonResponse({'success': False, 'message': 'Something went wrong. Please try again.'})


def admissions(request):
    """Admissions and registration page"""
    return render(request, 'core/admissions.html')


def student_resources(request):
    """Student resources page"""
    return render(request, 'core/student_resources.html')


def testimonials_page(request):
    """Dedicated testimonials page"""
    testimonials_list = Testimonial.objects.all()
    
    paginator = Paginator(testimonials_list, 12)
    page_number = request.GET.get('page')
    testimonials_page = paginator.get_page(page_number)
    
    context = {
        'testimonials': testimonials_page,
    }
    return render(request, 'core/testimonials.html', context)


@login_required
def enroll_course(request, slug):
    """Course enrollment page with payment method and installment selection"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    # Check if user is already enrolled
    existing_enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if existing_enrollment:
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('core:enrollment_status', enrollment_id=existing_enrollment.id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        installments = int(request.POST.get('installments', 1))
        selected_currency = request.POST.get('currency', 'KES')
        
        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('core:enroll_course', slug=course.slug)
        
        # Calculate total amount in selected currency
        total_amount = course.get_price_in_currency(selected_currency)
        
        # Create enrollment
        enrollment = Enrollment.objects.create(
            user=request.user,
            course=course,
            payment_method=payment_method,
            total_amount=total_amount,
            currency=selected_currency,
            installments=installments
        )
        
        # Create installment records
        installment_amount = total_amount / installments
        for i in range(installments):
            due_date = date.today() + timedelta(days=i * 30)  # Monthly installments
            PaymentInstallment.objects.create(
                enrollment=enrollment,
                installment_number=i + 1,
                amount=installment_amount,
                due_date=due_date
            )
        
        # Send enrollment email with payment instructions
        from emails.services import EmailService
        EmailService.send_enrollment_confirmation_email(
            user=request.user,
            course=course,
            enrollment=enrollment
        )
        
        messages.success(request, 'Enrollment created successfully! Check your email for payment instructions.')
        return redirect('core:enrollment_status', enrollment_id=enrollment.id)
    
    selected_currency = request.GET.get('currency', 'KES')
    currencies = [
        {'code': 'KES', 'name': 'Kenyan Shillings', 'symbol': 'KShs.'},
        {'code': 'USD', 'name': 'US Dollars', 'symbol': '$'},
        {'code': 'NGN', 'name': 'Nigerian Nairas', 'symbol': '₦'},
    ]
    
    context = {
        'course': course,
        'currencies': currencies,
        'selected_currency': selected_currency,
    }
    return render(request, 'core/enroll_course.html', context)


@login_required
def enrollment_status(request, enrollment_id):
    """Display enrollment status and payment instructions"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
    installments = enrollment.payment_installments.all()
    payment_instructions = enrollment.get_payment_instructions()
    
    context = {
        'enrollment': enrollment,
        'installments': installments,
        'payment_instructions': payment_instructions,
    }
    return render(request, 'core/enrollment_status.html', context)


@login_required 
def activate_enrollment(request):
    """Activate enrollment using activation code"""
    if request.method == 'POST':
        activation_code = request.POST.get('activation_code', '').strip().upper()
        
        if not activation_code:
            messages.error(request, 'Please enter an activation code.')
            return redirect('core:activate_enrollment')
        
        try:
            enrollment = Enrollment.objects.get(
                activation_code=activation_code,
                user=request.user,
                is_activated=False
            )
            enrollment.activate_enrollment()
            
            # Send welcome email
            from emails.services import EmailService
            EmailService.send_course_access_email(
                user=request.user,
                course=enrollment.course,
                enrollment=enrollment
            )
            
            messages.success(request, f'Congratulations! You have successfully activated your enrollment for {enrollment.course.title}.')
            return redirect('core:my_enrollments')
            
        except Enrollment.DoesNotExist:
            messages.error(request, 'Invalid activation code or this code has already been used.')
            return redirect('core:activate_enrollment')
    
    return render(request, 'core/activate_enrollment.html')


@login_required
def my_enrollments(request):
    """Display user's enrollments"""
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'core/my_enrollments.html', context)


def enroll_guest(request, slug):
    """Handle enrollment for non-authenticated users using unified registration form"""
    from accounts.forms import UnifiedRegistrationForm
    
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    if request.user.is_authenticated:
        return redirect('core:enroll_course', slug=course.slug)
    
    if request.method == 'POST':
        # Use unified registration form for consistent validation and field handling
        form = UnifiedRegistrationForm(request.POST, is_guest_enrollment=True)
        
        if form.is_valid():
            # Create user with immediate activation for guest enrollment
            user = form.save(commit=True, activate_immediately=True)
            
            # Log in the user immediately
            login(request, user)
            
            # Redirect to enrollment page
            messages.success(request, 'Account created successfully! Now you can proceed with enrollment.')
            return redirect('core:enroll_course', slug=course.slug)
        else:
            # If form has errors, show them to the user
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
    else:
        form = UnifiedRegistrationForm(is_guest_enrollment=True)
    
    context = {
        'course': course,
        'form': form,
    }
    return render(request, 'core/enroll_guest.html', context)
