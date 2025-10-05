# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:pk>/', views.notification_detail, name='detail'),
    path('<int:pk>/read/', views.mark_as_read, name='mark_read'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
    path('preferences/', views.notification_preferences, name='preferences'),
    path('unread-count/', views.get_unread_count, name='unread_count'),
]