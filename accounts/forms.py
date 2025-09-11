from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class CustomUserCreationForm(UserCreationForm):
    """Extended user creation form with email and name fields"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your last name'
        })
    )
    country = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your country'
        })
    )
    state_city = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your state/city'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'country', 'state_city', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Apply consistent styling to all fields
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Create a secure password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Confirm your password'
        })

        # Update help texts
        self.fields['username'].help_text = 'Required. 25 characters or fewer. Letters, digits and _ only.'
        self.fields['password1'].help_text = 'Your password must contain at least 8 characters and cannot be too similar to your personal information.'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with this email address already exists.')
        return email

    def clean_username(self):
        import re
        username = self.cleaned_data.get('username')
        
        # Check length
        if len(username) > 25:
            raise ValidationError('Username must be 25 characters or fewer.')
        
        # Check character pattern
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError('Username can only contain letters, digits, and underscores.')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            raise ValidationError('A user with this username already exists.')
        
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Update user profile with location data
            profile, created = user.userprofile
            if hasattr(user, 'userprofile'):
                user.userprofile.country = self.cleaned_data['country']
                user.userprofile.state_city = self.cleaned_data['state_city']
                user.userprofile.save()
        return user


class UserProfileForm(forms.ModelForm):
    """User profile editing form"""

    class Meta:
        model = UserProfile
        fields = [
            'phone_number', 'bio', 'profile_image', 'date_of_birth',
            'location', 'country', 'state_city', 'linkedin_profile', 'github_profile', 'website'
        ]
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter your phone number'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Tell us about yourself...',
                'rows': 4
            }),
            'profile_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'accept': 'image/*'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'type': 'date'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter your location'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter your country'
            }),
            'state_city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'Enter your state/city'
            }),
            'linkedin_profile': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'https://linkedin.com/in/yourprofile'
            }),
            'github_profile': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'https://github.com/yourusername'
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
                'placeholder': 'https://yourwebsite.com'
            }),
        }
        labels = {
            'phone_number': 'Phone Number',
            'bio': 'Biography',
            'profile_image': 'Profile Picture',
            'date_of_birth': 'Date of Birth',
            'location': 'Location',
            'country': 'Country',
            'state_city': 'State/City',
            'linkedin_profile': 'LinkedIn Profile',
            'github_profile': 'GitHub Profile',
            'website': 'Personal Website',
        }

    # Add user name fields
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your last name'
        })
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        if self.user:
            # Update user name fields
            self.user.first_name = self.cleaned_data.get('first_name', '')
            self.user.last_name = self.cleaned_data.get('last_name', '')
            if commit:
                self.user.save()

        # Check if profile is completed
        profile.profile_completed = profile.get_profile_completion_percentage() >= 80

        if commit:
            profile.save()

        return profile


class PasswordResetRequestForm(forms.Form):
    """Password reset request form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your email address'
        })
    )


class PasswordResetForm(forms.Form):
    """Password reset confirmation form"""
    password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your new password'
        })
    )
    password2 = forms.CharField(
        label='Confirm new password',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Confirm your new password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise ValidationError('The two password fields must match.')

            # Validate password strength
            password_validation.validate_password(password1)

        return cleaned_data


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Enter your username'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent pr-12',
            'placeholder': 'Enter your password'
        })