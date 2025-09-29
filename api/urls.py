from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, CompanyViewSet, JobViewSet, ApplicationViewSet
from .auth_views import AuthViewSet
from .dashboard_views import DashboardViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'applications', ApplicationViewSet)
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]


