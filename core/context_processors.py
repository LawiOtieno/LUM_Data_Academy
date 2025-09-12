
from django.contrib.auth.models import User
from .models import Course, BlogPost, Enrollment
from accounts.models import UserProfile

def admin_stats(request):
    """Context processor to provide statistics for admin dashboard"""
    if request.path.startswith('/admin/'):
        try:
            stats = {
                'user_count': User.objects.count(),
                'course_count': Course.objects.count(),
                'blog_count': BlogPost.objects.count(),
                'enrollment_count': Enrollment.objects.count(),
            }
            return stats
        except:
            # In case tables don't exist yet (during migrations)
            return {
                'user_count': 0,
                'course_count': 0,
                'blog_count': 0,
                'enrollment_count': 0,
            }
    return {}
