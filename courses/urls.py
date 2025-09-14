from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course listing and details
    path('', views.courses, name='courses'),
    
    # Enrollment system (put specific paths before slug patterns)
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),
    path('activate/', views.activate_enrollment, name='activate_enrollment'),
    path('enroll/<slug:slug>/', views.enroll_course, name='enroll_course'),
    path('enroll-guest/<slug:slug>/', views.enroll_guest, name='enroll_guest'),
    path('enrollment/<uuid:enrollment_id>/', views.enrollment_status, name='enrollment_status'),
    
    # Course details (put last since it catches any slug)
    path('<slug:slug>/', views.course_detail, name='course_detail'),
]