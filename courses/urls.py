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
    path('materials/<slug:slug>/', views.course_materials, name='course_materials'),
    path('materials/<slug:slug>/module/<int:module_id>/complete/', views.mark_module_complete, name='mark_module_complete'),
    path('materials/<slug:slug>/project/<int:project_id>/start/', views.start_project, name='start_project'),
    
    # Course details (put last since it catches any slug)
    path('<slug:slug>/', views.course_detail, name='course_detail'),
]