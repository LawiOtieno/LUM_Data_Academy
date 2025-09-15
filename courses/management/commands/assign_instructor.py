
"""
Management command to assign an instructor to courses
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from courses.models import Course


class Command(BaseCommand):
    help = 'Assign instructor to courses'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username of the instructor to assign to courses',
        )
        parser.add_argument(
            '--all-courses',
            action='store_true',
            help='Assign instructor to all courses without an instructor',
        )

    def handle(self, *args, **options):
        username = options.get('username')
        all_courses = options.get('all_courses')

        if not username:
            self.stdout.write(
                self.style.ERROR('Please provide a username with --username')
            )
            return

        try:
            instructor = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User with username "{username}" does not exist')
            )
            return

        if all_courses:
            # Assign to all courses without an instructor
            courses = Course.objects.filter(instructor__isnull=True)
            count = courses.update(instructor=instructor)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully assigned {instructor.username} as instructor to {count} courses'
                )
            )
        else:
            # Assign to all courses
            courses = Course.objects.all()
            count = courses.update(instructor=instructor)
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully assigned {instructor.username} as instructor to {count} courses'
                )
            )

        # List the courses that were updated
        updated_courses = Course.objects.filter(instructor=instructor)
        if updated_courses.exists():
            self.stdout.write('\nUpdated courses:')
            for course in updated_courses:
                self.stdout.write(f'  - {course.title}')
