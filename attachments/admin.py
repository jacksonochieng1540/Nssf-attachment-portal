# attachments/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Company, StudentProfile, Attachment
from .forms import AdminCompanyForm, StudentProfileForm

User = get_user_model()

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    form = AdminCompanyForm  # Use the admin form
    list_display = ('name', 'nssf_number', 'user', 'get_email')
    list_filter = ('name',)
    search_fields = ('name', 'nssf_number', 'user__username')
    raw_id_fields = ('user',)
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    form = StudentProfileForm
    list_display = ('user', 'student_id', 'department', 'get_email')
    list_filter = ('department',)
    search_fields = ('user__username', 'student_id', 'department')
    raw_id_fields = ('user',)
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'company', 'start_date', 'end_date', 'status', 'supervisor_name')
    list_filter = ('status', 'start_date', 'end_date', 'company')
    search_fields = ('student__user__username', 'company__name', 'supervisor_name')
    raw_id_fields = ('student', 'company')
    date_hierarchy = 'start_date'