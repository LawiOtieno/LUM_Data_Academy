from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admissions/', views.admissions, name='admissions'),
    path('student-resources/', views.student_resources, name='student_resources'),

    # Events
    path('events/', views.events, name='events'),
    path('event/<slug:slug>/', views.event_detail, name='event_detail'),

    # Blog
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

    # Testimonials
    path('testimonials/', views.testimonials_page, name='testimonials'),

    # AJAX endpoints
    path('api/newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),

    # Legal & Info Pages
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('payment-policy/', views.payment_policy, name='payment_policy'),
    path('faqs/', views.faqs, name='faqs'),

    # Careers
    path('careers/', views.careers, name='careers'),
    path('career/<slug:slug>/', views.career_detail, name='career_detail'),

    # Surveys
    path('surveys/', views.surveys, name='surveys'),
    path('survey/<slug:slug>/', views.survey_detail, name='survey_detail'),
]