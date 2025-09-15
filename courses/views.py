from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import timedelta, date
import json

from .models import Course, CourseCategory, Enrollment, PaymentInstallment, ModuleCompletion, ProjectEnrollment
from .forms import ProjectSubmissionForm, InstructorReviewForm


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

        except Enrollment.DoesNotExist:
            messages.error(request, 'Invalid activation code or this code has already been used.')
            return redirect('courses:activate_enrollment')

    return render(request, 'courses/activate_enrollment.html')


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
    
    # Get completion data
    completed_modules = enrollment.module_completions.values_list('module_id', flat=True)
    started_projects = enrollment.project_enrollments.values_list('project_id', flat=True)
    
    # Add completion status to modules
    for module in modules:
        module.is_completed = module.id in completed_modules
    
    # Add enrollment status and enrollment object to projects
    project_enrollments = {pe.project_id: pe for pe in enrollment.project_enrollments.all()}
    for project in capstone_projects:
        project.is_started = project.id in started_projects
        project.project_enrollment = project_enrollments.get(project.id)
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'modules': modules,
        'capstone_projects': capstone_projects,
        'total_modules': modules.count(),
        'completed_modules_count': len(completed_modules),
    }
    return render(request, 'courses/course_materials.html', context)


@login_required
def my_enrollments(request):
    """Display user's enrollments"""
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'enrollments': enrollments,
    }
    return render(request, 'courses/my_enrollments.html', context)


@login_required
@require_http_methods(["POST"])
def mark_module_complete(request, slug, module_id):
    """Mark a module as complete for the user"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    module = get_object_or_404(course.modules, id=module_id, is_active=True)
    
    # Check if user has active enrollment
    try:
        enrollment = Enrollment.objects.get(
            user=request.user, 
            course=course, 
            is_activated=True
        )
    except Enrollment.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No active enrollment found'})
    
    # Create or get module completion record
    completion, created = ModuleCompletion.objects.get_or_create(
        enrollment=enrollment,
        module=module,
        defaults={'completed_at': timezone.now()}
    )
    
    if not created:
        # If already completed, mark as incomplete (toggle)
        completion.delete()
        completed = False
        message = f"Module {module.order} marked as incomplete"
    else:
        completed = True
        message = f"Congratulations! Module {module.order} completed"
    
    # Get updated completion count
    completed_modules = ModuleCompletion.objects.filter(enrollment=enrollment).count()
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'success': True,
            'completed': completed,
            'message': message,
            'completed_modules': completed_modules
        })
    
    messages.success(request, message)
    return redirect('courses:course_materials', slug=course.slug)


@login_required
@require_http_methods(["POST"])
def start_project(request, slug, project_id):
    """Start a capstone project"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    project = get_object_or_404(course.capstone_projects, id=project_id)
    
    # Check if user has active enrollment
    try:
        enrollment = Enrollment.objects.get(
            user=request.user, 
            course=course, 
            is_activated=True
        )
    except Enrollment.DoesNotExist:
        messages.error(request, 'You do not have access to this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    # Create or get project enrollment
    project_enrollment, created = ProjectEnrollment.objects.get_or_create(
        enrollment=enrollment,
        project=project,
        defaults={'started_at': timezone.now()}
    )
    
    if created:
        message = f"Project '{project.title}' started successfully! Good luck!"
        messages.success(request, message)
    else:
        message = f"You have already started project '{project.title}'"
        messages.info(request, message)
    
    if request.headers.get('Accept') == 'application/json':
        return JsonResponse({
            'success': True,
            'message': message,
            'started': created
        })
    
    return redirect('courses:course_materials', slug=course.slug)


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


@login_required
def submit_project(request, slug, project_id):
    """Submit a capstone project with links to GitHub, Colab, etc."""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    project = get_object_or_404(course.capstone_projects, id=project_id)
    
    # Check if user has active enrollment
    try:
        enrollment = Enrollment.objects.get(
            user=request.user, 
            course=course, 
            is_activated=True
        )
    except Enrollment.DoesNotExist:
        messages.error(request, 'You do not have access to this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    # Get or create project enrollment
    try:
        project_enrollment = ProjectEnrollment.objects.get(
            enrollment=enrollment,
            project=project
        )
    except ProjectEnrollment.DoesNotExist:
        messages.error(request, 'Please start the project first before submitting.')
        return redirect('courses:course_materials', slug=course.slug)
    
    # Check if project can be submitted
    if project_enrollment.status not in ['in_progress', 'submitted']:
        messages.error(request, f'Project cannot be submitted. Current status: {project_enrollment.get_status_display()}')
        return redirect('courses:course_materials', slug=course.slug)
    
    if request.method == 'POST':
        form = ProjectSubmissionForm(request.POST)
        if form.is_valid():
            # Submit the project with form data
            submission_data = {
                'submission_notes': form.cleaned_data['submission_notes'],
                'github_repo_url': form.cleaned_data['github_repo_url'],
                'google_colab_url': form.cleaned_data['google_colab_url'],
                'jupyter_notebook_url': form.cleaned_data['jupyter_notebook_url'],
                'additional_links': form.cleaned_data['additional_links'],
            }
            
            project_enrollment.submit_project(submission_data)
            
            # Send notification email to instructor
            from emails.services import EmailService
            EmailService.send_project_submission_notification(project_enrollment)
            
            messages.success(request, f'Project "{project.title}" submitted successfully! Your instructor will review it shortly.')
            return redirect('courses:course_materials', slug=course.slug)
    else:
        # Pre-fill form with existing data if already submitted
        initial_data = {}
        if project_enrollment.status == 'submitted':
            initial_data = {
                'submission_notes': project_enrollment.submission_notes,
                'github_repo_url': project_enrollment.github_repo_url,
                'google_colab_url': project_enrollment.google_colab_url,
                'jupyter_notebook_url': project_enrollment.jupyter_notebook_url,
                'additional_links': project_enrollment.additional_links,
            }
        form = ProjectSubmissionForm(initial=initial_data)
    
    context = {
        'course': course,
        'project': project,
        'project_enrollment': project_enrollment,
        'form': form,
        'is_resubmission': project_enrollment.status == 'submitted',
    }
    return render(request, 'courses/submit_project.html', context)


@login_required
def instructor_review_project(request, slug, project_id, enrollment_id):
    """Instructor interface to review and complete submitted projects"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    project = get_object_or_404(course.capstone_projects, id=project_id)
    
    # Check if user is instructor for this course
    if not (request.user.is_staff or request.user == course.instructor):
        messages.error(request, 'You do not have permission to review projects for this course.')
        return redirect('courses:course_detail', slug=course.slug)
    
    # Get the project enrollment
    project_enrollment = get_object_or_404(
        ProjectEnrollment,
        id=enrollment_id,
        project=project,
        status='submitted'
    )
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'complete':
            form = InstructorReviewForm(request.POST, instance=project_enrollment)
            if form.is_valid():
                # Complete the project
                form.save()
                project_enrollment.complete_project(
                    grade=form.cleaned_data.get('grade'),
                    instructor=request.user
                )
                
                # Send completion notification email
                from emails.services import EmailService
                EmailService.send_project_completion_notification(project_enrollment)
                
                messages.success(request, f'Project completed successfully. Certificate has been generated for {project_enrollment.enrollment.user.get_full_name()}.')
                return redirect('courses:instructor_review_project', slug=course.slug, project_id=project_id, enrollment_id=enrollment_id)
        
        elif action == 'request_changes':
            # Set status back to in_progress for resubmission
            project_enrollment.status = 'in_progress'
            project_enrollment.save()
            
            messages.success(request, 'Project returned for revisions. Student has been notified.')
            return redirect('courses:instructor_review_project', slug=course.slug, project_id=project_id, enrollment_id=enrollment_id)
    
    form = InstructorReviewForm(instance=project_enrollment)
    
    context = {
        'course': course,
        'project': project,
        'project_enrollment': project_enrollment,
        'form': form,
        'submission_links': project_enrollment.get_submission_links(),
    }
    return render(request, 'courses/instructor_review.html', context)


@login_required
def download_certificate(request, enrollment_id):
    """Download project completion certificate"""
    project_enrollment = get_object_or_404(
        ProjectEnrollment,
        id=enrollment_id,
        enrollment__user=request.user,
        status='completed'
    )
    
    if not project_enrollment.can_download_certificate():
        messages.error(request, 'Certificate is not available for download.')
        return redirect('courses:course_materials', slug=project_enrollment.enrollment.course.slug)
    
    # Increment download count
    project_enrollment.certificate_download_count += 1
    project_enrollment.save()
    
    # Return the certificate file
    try:
        response = HttpResponse(
            project_enrollment.certificate_file.read(),
            content_type='application/pdf'
        )
        filename = f"LUM_Certificate_{project_enrollment.enrollment.user.username}_{project_enrollment.project.title.replace(' ', '_')}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    except Exception as e:
        messages.error(request, 'Error downloading certificate. Please contact support.')
        return redirect('courses:course_materials', slug=project_enrollment.enrollment.course.slug)


@login_required
def instructor_dashboard(request):
    """Dashboard for instructors to view all submitted projects"""
    if not request.user.is_staff:
        # Check if user is an instructor for any courses
        instructor_courses = Course.objects.filter(instructor=request.user, is_active=True)
        if not instructor_courses.exists():
            messages.error(request, 'You do not have instructor permissions.')
            return redirect('courses:courses')
    else:
        # Staff can see all courses
        instructor_courses = Course.objects.filter(is_active=True)
    
    # Get all submitted projects for instructor's courses
    submitted_projects = ProjectEnrollment.objects.filter(
        project__course__in=instructor_courses,
        status='submitted'
    ).select_related(
        'enrollment__user',
        'enrollment__course',
        'project'
    ).order_by('-submitted_at')
    
    context = {
        'instructor_courses': instructor_courses,
        'submitted_projects': submitted_projects,
    }
    return render(request, 'courses/instructor_dashboard.html', context)