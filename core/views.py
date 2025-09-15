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
from django.db.models import Q
from decimal import Decimal

from courses.models import Course
from .models import (
    Testimonial, Event, BlogPost, ContactSubmission, 
    Newsletter, AboutPage, Career, Survey
)
from .forms import ContactForm, NewsletterForm


def home(request):
    """Modern homepage with dynamic content"""
    # Get featured courses that are active, prioritizing those with discounts
    featured_courses = Course.objects.filter(is_featured=True, is_active=True).order_by(
        '-discount_price', '-created_at'
    )[:3]
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
    """Admissions and registration page with featured courses"""
    # Get featured courses for the admissions page
    featured_courses = Course.objects.filter(
        is_featured=True, 
        is_active=True,
        is_published=True
    ).order_by('-discount_price', '-created_at')[:6]
    
    context = {
        'featured_courses': featured_courses,
    }
    return render(request, 'core/admissions.html', context)


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


def enroll_guest(request, slug):
    """Handle enrollment for non-authenticated users using unified registration form"""
    from accounts.forms import UnifiedRegistrationForm

    course = get_object_or_404(Course, slug=slug, is_active=True)

    if request.user.is_authenticated:
        return redirect('courses:enroll_course', slug=course.slug)

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
            return redirect('courses:enroll_course', slug=course.slug)
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


def terms_of_service(request):
    """Terms of Service page"""
    return render(request, 'core/terms_of_service.html')


def privacy_policy(request):
    """Privacy Policy page"""
    return render(request, 'core/privacy_policy.html')


def payment_policy(request):
    """Payment Policy page"""
    return render(request, 'core/payment_policy.html')


def faqs(request):
    """Frequently Asked Questions page"""
    return render(request, 'core/faqs.html')


def careers(request):
    """Careers page listing all open positions"""
    careers_list = Career.objects.filter(is_active=True)

    # Filter by department if specified
    department = request.GET.get('department')
    if department:
        careers_list = careers_list.filter(department__icontains=department)

    # Filter by job type if specified
    job_type = request.GET.get('type')
    if job_type:
        careers_list = careers_list.filter(job_type=job_type)

    paginator = Paginator(careers_list, 10)
    page_number = request.GET.get('page')
    careers_page = paginator.get_page(page_number)

    # Get unique departments for filter
    departments = Career.objects.filter(is_active=True).values_list('department', flat=True).distinct()

    context = {
        'careers': careers_page,
        'departments': departments,
        'current_department': department,
        'current_job_type': job_type,
    }
    return render(request, 'core/careers.html', context)


def career_detail(request, slug):
    """Individual career detail page"""
    career = get_object_or_404(Career, slug=slug, is_active=True)
    related_careers = Career.objects.filter(
        department=career.department, 
        is_active=True
    ).exclude(id=career.id)[:3]

    context = {
        'career': career,
        'related_careers': related_careers,
    }
    return render(request, 'core/career_detail.html', context)


def surveys(request):
    """Surveys page listing all active surveys"""
    surveys_list = Survey.objects.filter(is_active=True)

    # Filter by survey type if specified
    survey_type = request.GET.get('type')
    if survey_type:
        surveys_list = surveys_list.filter(survey_type=survey_type)

    paginator = Paginator(surveys_list, 10)
    page_number = request.GET.get('page')
    surveys_page = paginator.get_page(page_number)

    # Get survey types for filter
    survey_types = Survey.objects.filter(is_active=True).values_list('survey_type', flat=True).distinct()

    context = {
        'surveys': surveys_page,
        'survey_types': survey_types,
        'current_survey_type': survey_type,
    }
    return render(request, 'core/surveys.html', context)


def survey_detail(request, slug):
    """Individual survey detail page"""
    survey = get_object_or_404(Survey, slug=slug, is_active=True)

    if not survey.is_open():
        messages.info(request, 'This survey is currently not accepting responses.')

    context = {
        'survey': survey,
    }
    return render(request, 'core/survey_detail.html', context)