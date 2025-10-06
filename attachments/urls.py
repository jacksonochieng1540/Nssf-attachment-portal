from django.urls import path
from . import views

urlpatterns = [
    path('', views.attachment_list, name='attachment_list'),
    path('create/', views.attachment_create, name='attachment_create'),
    path('<int:pk>/', views.attachment_detail, name='attachment_detail'),
    path('<int:pk>/update/', views.attachment_update, name='attachment_update'),
    path('<int:pk>/delete/', views.attachment_delete, name='attachment_delete'),
    path('<int:pk>/approve/', views.attachment_approve, name='attachment_approve'),
    path('<int:pk>/reject/', views.attachment_reject, name='attachment_reject'),
    path('stats/', views.attachment_stats, name='attachment_stats'),
    
    # Company urls
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),  
    path('companies/register/', views.company_register, name='company_register'),
    path('companies/<int:pk>/update/', views.company_update, name='company_update'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),
    
    
    # Student profile urls
    path('students/', views.student_list, name='student_list'),
    path('students/create/', views.student_profile_create, name='student_profile_create'),
    path('student/profile/create/', views.create_student_profile, name='create_student_profile'),
    path('students/<int:pk>/update/', views.student_profile_update, name='student_profile_update'),
    path('students/<int:pk>/delete/', views.student_profile_delete, name='student_profile_delete'),
]

