from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from django.conf import settings
import json

from .models import UserProfile, MathCaptcha, EmailVerificationToken, PasswordResetToken
from .utils import (
    generate_math_captcha, verify_math_captcha,
    send_verification_email, send_password_reset_email, clean_expired_tokens
)
from .forms import (
    UnifiedRegistrationForm, CustomUserCreationForm, UserProfileForm,
    PasswordResetRequestForm, PasswordResetForm
)


def generate_captcha_ajax(request):
    """Generate new math captcha via AJAX"""
    if not request.session.session_key:
        request.session.create()

    captcha = generate_math_captcha(request.session.session_key)
    return JsonResponse({
        'question': captcha.question,
        'success': True
    })


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if not request.session.session_key:
        request.session.create()

    # Generate initial captcha
    captcha = generate_math_captcha(request.session.session_key)

    if request.method == 'POST':
        form = UnifiedRegistrationForm(request.POST)
        captcha_answer = request.POST.get('captcha_answer', '')

        # Verify captcha first
        captcha_valid, captcha_message = verify_math_captcha(
            request.session.session_key, captcha_answer
        )

        if not captcha_valid:
            messages.error(request, captcha_message)
            # Generate new captcha for retry
            captcha = generate_math_captcha(request.session.session_key)
        elif form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    user.is_active = False  # User must verify email first
                    user.save()

                    # Send verification email
                    success, message = send_verification_email(user, request)
                    if success:
                        messages.success(
                            request,
                            f'Registration successful! Please check your email ({user.email}) '
                            'for a verification link to activate your account.'
                        )
                        return redirect('accounts:login')
                    else:
                        messages.error(request, f'Registration successful but {message}')
                        return redirect('accounts:login')

            except Exception as e:
                messages.error(request, f'Registration failed: {str(e)}')
                captcha = generate_math_captcha(request.session.session_key)
        else:
            # Generate new captcha if form is invalid
            captcha = generate_math_captcha(request.session.session_key)
    else:
        form = UnifiedRegistrationForm()

    context = {
        'form': form,
        'captcha': captcha,
    }
    return render(request, 'accounts/register.html', context)


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                if not user.is_active:
                    messages.error(
                        request,
                        'Your account is not activated. Please check your email for '
                        'the verification link or contact support.'
                    )
                    return render(request, 'accounts/login.html', {'form': form})

                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')

                # Redirect to next page or dashboard
                next_page = request.GET.get('next', 'accounts:dashboard')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """User logout view"""
    if request.user.is_authenticated:
        messages.success(request, 'You have been successfully logged out.')
    logout(request)
    return redirect('core:home')


def verify_email(request, token):
    """Email verification view"""
    try:
        verification_token = get_object_or_404(EmailVerificationToken, token=token)

        if verification_token.is_used:
            messages.warning(request, 'This verification link has already been used.')
            return redirect('accounts:login')

        if verification_token.is_expired():
            messages.error(
                request,
                'This verification link has expired. Please request a new one.'
            )
            verification_token.delete()
            return redirect('accounts:login')

        # Activate user account
        user = verification_token.user
        user.is_active = True
        user.save()

        # Mark email as verified
        user.userprofile.is_email_verified = True
        user.userprofile.save()

        # Mark token as used
        verification_token.is_used = True
        verification_token.save()

        messages.success(
            request,
            'Email verified successfully! You can now log in to your account.'
        )
        return redirect('accounts:login')

    except Exception as e:
        messages.error(request, 'Invalid verification link.')
        return redirect('accounts:login')


@login_required
def dashboard(request):
    """Main dashboard view - redirects based on user role"""
    profile = request.user.userprofile

    if profile.is_instructor:
        return redirect('accounts:instructor_dashboard')
    else:
        return redirect('accounts:learner_dashboard')


def learner_dashboard(request):
    """Learner-specific dashboard"""
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    # Import here to avoid circular imports
    from courses.models import Enrollment

    # Get user's enrollments
    enrollments = Enrollment.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'enrollments': enrollments,
    }
    return render(request, 'accounts/learner_dashboard.html', context)


@login_required
def instructor_dashboard(request):
    """Instructor dashboard"""
    profile = request.user.userprofile

    # Only instructors can access this
    if not profile.is_instructor:
        messages.error(request, 'Access denied. Instructor privileges required.')
        return redirect('accounts:learner_dashboard')

    # Get instructor's courses (mock for now)
    try:
        from courses.models import Course
        instructor_courses = Course.objects.filter(is_published=True)[:3]  # Mock for now
    except:
        instructor_courses = []

    context = {
        'profile': profile,
        'instructor_courses': instructor_courses,
        'completion_percentage': profile.get_profile_completion_percentage(),
    }
    return render(request, 'accounts/instructor_dashboard.html', context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES,
                              instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:dashboard')
    else:
        form = UserProfileForm(instance=profile, user=request.user)

    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'accounts/profile_edit.html', context)


def password_reset_request(request):
    """Password reset request"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                success, message = send_password_reset_email(user, request)
                if success:
                    messages.success(
                        request,
                        'Password reset instructions have been sent to your email.'
                    )
                else:
                    messages.error(request, message)
            except User.DoesNotExist:
                # For security, don't reveal if email exists
                messages.success(
                    request,
                    'If an account with this email exists, password reset '
                    'instructions have been sent.'
                )
            return redirect('accounts:login')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'accounts/password_reset_request.html', {'form': form})


def password_reset_confirm(request, token):
    """Password reset confirmation"""
    try:
        reset_token = get_object_or_404(PasswordResetToken, token=token)

        if reset_token.is_used:
            messages.error(request, 'This password reset link has already been used.')
            return redirect('accounts:login')

        if reset_token.is_expired():
            messages.error(request, 'This password reset link has expired.')
            reset_token.delete()
            return redirect('accounts:password_reset_request')

        if request.method == 'POST':
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                # Set new password
                user = reset_token.user
                user.set_password(form.cleaned_data['password1'])
                user.save()

                # Mark token as used
                reset_token.is_used = True
                reset_token.save()

                messages.success(
                    request,
                    'Password reset successfully! You can now log in with your new password.'
                )
                return redirect('accounts:login')
        else:
            form = PasswordResetForm()

        context = {
            'form': form,
            'token': token,
        }
        return render(request, 'accounts/password_reset_confirm.html', context)

    except Exception as e:
        messages.error(request, 'Invalid password reset link.')
        return redirect('accounts:login')


@login_required
def resend_verification(request):
    """Resend email verification"""
    if request.user.userprofile.is_email_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('accounts:dashboard')

    success, message = send_verification_email(request.user, request)
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)

    return redirect('accounts:dashboard')