
from django.urls import path
from . import views

app_name = 'emails'

urlpatterns = [
    path('test/', views.test_email_system, name='test_system'),
]
