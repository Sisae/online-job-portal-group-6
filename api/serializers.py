from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import UserProfile
from companies.models import Company
from jobs.models import Job
from applications.models import Application


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_type', 'phone_number', 'bio', 'location', 'profile_picture', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class CompanySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    jobs_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Company
        fields = ['id', 'name', 'website', 'description', 'logo', 'location', 'contact_email', 'owner', 'created_at', 'updated_at', 'jobs_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'jobs_count']
    
    def get_jobs_count(self, obj):
        return obj.jobs.count()


class JobSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)
    company_id = serializers.IntegerField(write_only=True)
    created_by = UserSerializer(read_only=True)
    application_count = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'slug', 'description', 'company', 'company_id', 
            'location', 'remote', 'job_type', 'salary', 'posted_date', 
            'closing_date', 'is_active', 'created_by', 'created_at', 
            'updated_at', 'application_count', 'is_open'
        ]
        read_only_fields = ['id', 'slug', 'created_by', 'created_at', 'updated_at', 'application_count', 'is_open']
    
    def get_application_count(self, obj):
        return obj.applications.count()
    
    def get_is_open(self, obj):
        return obj.is_open()


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            'title', 'description', 'location', 'remote', 'job_type', 
            'salary', 'closing_date', 'is_active'
        ]
    
    def create(self, validated_data):
        # Set the company to the user's company
        user = self.context['request'].user
        if hasattr(user, 'company'):
            validated_data['company'] = user.company
        else:
            raise serializers.ValidationError("User must have a company profile to create jobs")
        
        validated_data['created_by'] = user
        return super().create(validated_data)


class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    job_id = serializers.IntegerField(write_only=True)
    applicant = UserSerializer(read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    status_class = serializers.CharField(source='get_status_display_class', read_only=True)
    
    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_id', 'applicant', 'status', 'status_display', 
            'status_class', 'cover_letter', 'resume', 'applied_date', 
            'updated_at', 'notes'
        ]
        read_only_fields = ['id', 'applicant', 'applied_date', 'updated_at']


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['cover_letter', 'resume']
    
    def create(self, validated_data):
        job_id = self.context['job_id']
        user = self.context['request'].user
        
        # Check if user already applied
        if Application.objects.filter(job_id=job_id, applicant=user).exists():
            raise serializers.ValidationError("You have already applied for this job")
        
        validated_data['job_id'] = job_id
        validated_data['applicant'] = user
        return super().create(validated_data)


class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status', 'notes']
    
    def update(self, instance, validated_data):
        # Send email notification if status changed
        old_status = instance.status
        response = super().update(instance, validated_data)
        
        if old_status != instance.status:
            # Import here to avoid circular imports
            from applications.views import ApplicationStatusUpdateView
            view = ApplicationStatusUpdateView()
            view.object = instance
            view.send_status_notification(old_status, instance.status)
        
        return response


class DashboardStatsSerializer(serializers.Serializer):
    total_jobs = serializers.IntegerField()
    active_jobs = serializers.IntegerField()
    total_applications = serializers.IntegerField()
    pending_applications = serializers.IntegerField()
    recent_applications = ApplicationSerializer(many=True)
    recent_jobs = JobSerializer(many=True)

