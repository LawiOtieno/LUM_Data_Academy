from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile


class UnifiedRegistrationForm(UserCreationForm):
    """Unified registration form that can be used for both regular and guest enrollment"""
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
    
    # Optional fields for enhanced registration
    marketing_consent = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'mr-2'}),
        label="I'd like to receive updates about new courses and special offers"
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'country', 'state_city', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        # Extract configuration options
        self.skip_password_confirmation = kwargs.pop('skip_password_confirmation', False)
        self.is_guest_enrollment = kwargs.pop('is_guest_enrollment', False)
        super().__init__(*args, **kwargs)

        # Apply consistent styling to all fields
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Choose a unique username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Create a secure password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent',
            'placeholder': 'Confirm your password'
        })
        
        # For guest enrollment, we can make password2 optional
        if self.skip_password_confirmation:
            self.fields['password2'].required = False
            self.fields['password2'].widget.attrs.update({'style': 'display: none;'})
            
        # Add additional styling for guest enrollment
        if self.is_guest_enrollment:
            for field_name, field in self.fields.items():
                if hasattr(field.widget, 'attrs'):
                    field.widget.attrs.update({
                        'class': field.widget.attrs.get('class', '').replace('focus:ring-primary', 'focus:ring-2 focus:ring-primary')
                    })

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('A user with that username already exists.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with that email address already exists.')
        return email

    def save(self, commit=True, activate_immediately=False):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Set activation status based on parameters
        if activate_immediately:
            user.is_active = True
        else:
            user.is_active = False  # Email verification required

        if commit:
            user.save()
            
            # Create or update user profile
            from .models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.country = self.cleaned_data.get('country', '')
            profile.state_city = self.cleaned_data.get('state_city', '')
            profile.save()
            
        return user


# Keep the old form name for backward compatibility
class CustomUserCreationForm(UnifiedRegistrationForm):
    """Legacy form name - redirects to UnifiedRegistrationForm for backward compatibility"""
    pass


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