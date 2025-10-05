# reports/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_report, name='generate_report'),
    path('download/<str:report_type>/', views.download_report, name='download_report'),
]