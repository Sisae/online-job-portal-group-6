from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from jobs.models import Job
from applications.models import Application


class Command(BaseCommand):
    help = 'Create test applications for existing jobs'

    def handle(self, *args, **options):
        # Create test users if they don't exist
        test_users = [
            {'username': 'testuser1', 'email': 'test1@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'testuser2', 'email': 'test2@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'testuser3', 'email': 'test3@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
        ]
        
        for user_data in test_users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
        
        # Get all jobs
        jobs = Job.objects.all()
        
        if not jobs.exists():
            self.stdout.write(self.style.WARNING('No jobs found. Please create some jobs first.'))
            return
        
        # Create test applications
        applications_created = 0
        for job in jobs:
            for i, user_data in enumerate(test_users):
                user = User.objects.get(username=user_data['username'])
                
                # Check if application already exists
                if not Application.objects.filter(job=job, applicant=user).exists():
                    application = Application.objects.create(
                        job=job,
                        applicant=user,
                        status='applied',
                        cover_letter=f'Dear Hiring Manager,\n\nI am writing to express my interest in the {job.title} position at {job.company.name}. I believe my skills and experience make me a strong candidate for this role.\n\nBest regards,\n{user.get_full_name()}'
                    )
                    applications_created += 1
                    self.stdout.write(f'Created application: {user.get_full_name()} for {job.title}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {applications_created} test applications')
        )


