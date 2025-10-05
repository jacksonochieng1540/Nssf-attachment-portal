from django.urls import path
from . import views

urlpatterns = [
    path('details/', views.nssf_detail, name='nssf_detail'),
    path('details/update/', views.nssf_detail_update, name='nssf_detail_update'),
    path('returns/', views.nssf_return_list, name='nssf_return_list'),
    path('returns/create/', views.nssf_return_create, name='nssf_return_create'),
    path('returns/<int:pk>/', views.nssf_return_detail, name='nssf_return_detail'),
]