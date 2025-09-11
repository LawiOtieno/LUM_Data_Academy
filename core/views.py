
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Course, CourseCategory, Testimonial, Event, BlogPost, ContactSubmission, Newsletter, AboutPage
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
    
    courses_list = Course.objects.filter(is_active=True)
    
    if category_slug:
        courses_list = courses_list.filter(category__name=category_slug)
    
    if search_query:
        courses_list = courses_list.filter(title__icontains=search_query)
    
    paginator = Paginator(courses_list, 9)
    page_number = request.GET.get('page')
    courses_page = paginator.get_page(page_number)
    
    context = {
        'courses': courses_page,
        'categories': categories,
        'current_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'core/courses.html', context)


def course_detail(request, slug):
    """Individual course detail page"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    related_courses = Course.objects.filter(
        category=course.category, 
        is_active=True
    ).exclude(id=course.id)[:3]
    
    context = {
        'course': course,
        'related_courses': related_courses,
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
