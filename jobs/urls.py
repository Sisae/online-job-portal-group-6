from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('create/', views.JobCreateView.as_view(), name='job_create'),
    path('<slug:slug>/', views.JobDetailView.as_view(), name='job_detail'),
    path('<slug:slug>/edit/', views.JobEditView.as_view(), name='job_edit'),
    path('<slug:slug>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
]
