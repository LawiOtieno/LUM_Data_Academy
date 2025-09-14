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

from .models import Course, CourseCategory, Enrollment, PaymentInstallment


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
    return render(request, 'courses/courses.html', context)


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
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    """Course enrollment page with payment method and installment selection"""
    course = get_object_or_404(Course, slug=slug, is_active=True)

    # Check if user is already enrolled
    existing_enrollment = Enrollment.objects.filter(user=request.user, course=course).first()
    if existing_enrollment:
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('courses:enrollment_status', enrollment_id=existing_enrollment.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        installments = int(request.POST.get('installments', 1))
        selected_currency = request.POST.get('currency', 'KES')

        if not payment_method:
            messages.error(request, 'Please select a payment method.')
            return redirect('courses:enroll_course', slug=course.slug)

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
        return redirect('courses:enrollment_status', enrollment_id=enrollment.id)

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
    return render(request, 'courses/enroll_course.html', context)


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
    return render(request, 'courses/enrollment_status.html', context)


@login_required
def activate_enrollment(request):
    """Activate enrollment using activation code"""
    if request.method == 'POST':
        activation_code = request.POST.get('activation_code', '').strip().upper()

        if not activation_code:
            messages.error(request, 'Please enter an activation code.')
            return redirect('courses:activate_enrollment')

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
            return redirect('courses:my_enrollments')



@login_required
def course_materials(request, slug):
    """Access course materials for enrolled and activated users"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    # Check if user has active enrollment
    try:
        enrollment = Enrollment.objects.get(
            user=request.user, 
            course=course, 
            is_activated=True
        )
    except Enrollment.DoesNotExist:
        messages.error(request, 'You do not have access to this course. Please ensure your enrollment is activated.')
        return redirect('courses:course_detail', slug=course.slug)
    
    # Get course modules and content
    modules = course.modules.filter(is_active=True).order_by('order')
    capstone_projects = course.capstone_projects.all().order_by('order')
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'modules': modules,
        'capstone_projects': capstone_projects,
        'total_modules': modules.count(),
    }
    return render(request, 'courses/course_materials.html', context)

        except Enrollment.DoesNotExist:
            messages.error(request, 'Invalid activation code or this code has already been used.')
            return redirect('courses:activate_enrollment')

    return render(request, 'courses/activate_enrollment.html')


@login_required
def my_enrollments(request):
    """Display user's enrollments"""
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'enrollments': enrollments,
    }
    return render(request, 'courses/my_enrollments.html', context)


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
    return render(request, 'courses/enroll_guest.html', context)