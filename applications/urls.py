from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('', views.ApplicationListView.as_view(), name='application_list'),
    path('<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('<int:pk>/update-status/', views.ApplicationStatusUpdateView.as_view(), name='application_status_update'),
]
