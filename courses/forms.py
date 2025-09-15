"""
Forms for course-related functionality including project submissions
"""
from django import forms
from django.contrib.auth.models import User
from .models import ProjectEnrollment


class ProjectSubmissionForm(forms.Form):
    """Form for students to submit their capstone projects"""

    submission_notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Describe your project, approach, and key findings...',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'
        }),
        label='Project Description & Notes',
        help_text='Provide a brief description of your project, your approach, and key findings.',
        required=True
    )

    github_repo_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'https://github.com/username/repository',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'
        }),
        label='GitHub Repository URL',
        help_text='Link to your GitHub repository containing the project code.',
        required=False
    )

    google_colab_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'https://colab.research.google.com/drive/...',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'
        }),
        label='Google Colab Notebook URL',
        help_text='Link to your Google Colab notebook (make sure it\'s publicly accessible).',
        required=False
    )

    jupyter_notebook_url = forms.URLField(
        widget=forms.URLInput(attrs={
            'placeholder': 'https://jupyter.org/try or your notebook URL',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'
        }),
        label='Jupyter Notebook URL',
        help_text='Link to your Jupyter notebook file or online notebook.',
        required=False
    )

    additional_links = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'Any additional links or resources (one per line)...',
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'
        }),
        label='Additional Links',
        help_text='Any other relevant links like datasets, documentation, or presentations.',
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        github_repo = cleaned_data.get('github_repo_url')
        colab_url = cleaned_data.get('google_colab_url')
        jupyter_url = cleaned_data.get('jupyter_notebook_url')
        additional_links = cleaned_data.get('additional_links')

        # At least one submission link is required
        if not any([github_repo, colab_url, jupyter_url, additional_links]):
            raise forms.ValidationError(
                'Please provide at least one project link (GitHub, Google Colab, Jupyter Notebook, or Additional Links).'
            )

        return cleaned_data


class InstructorReviewForm(forms.ModelForm):
    """Form for instructors to review and grade submitted projects"""

    class Meta:
        model = ProjectEnrollment
        fields = ['instructor_feedback', 'grade']
        widgets = {
            'instructor_feedback': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': 'Provide detailed feedback on the project...',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'
            }),
            'grade': forms.NumberInput(attrs={
                'min': 0,
                'max': 100,
                'placeholder': 'Enter grade (0-100)',
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-blue-500'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['instructor_feedback'].label = 'Feedback & Comments'
        self.fields['instructor_feedback'].help_text = 'Provide constructive feedback on the project quality, approach, and areas for improvement.'
        self.fields['grade'].label = 'Grade (0-100)'
        self.fields['grade'].help_text = 'Enter a numerical grade between 0 and 100.'

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if grade is not None:
            if grade < 0 or grade > 100:
                raise forms.ValidationError('Grade must be between 0 and 100.')
        return grade