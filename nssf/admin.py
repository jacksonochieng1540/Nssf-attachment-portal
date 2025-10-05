# nssf/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import NSSFDetail, NSSFReturn

@admin.register(NSSFDetail)
class NSSFDetailAdmin(admin.ModelAdmin):
    list_display = ('student', 'nssf_number', 'is_verified', 'verification_status', 'created_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('student__user__username', 'student__student_id', 'nssf_number')
    raw_id_fields = ('student', 'verified_by')
    readonly_fields = ('created_at', 'updated_at', 'verification_status')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Student Information', {
            'fields': ('student', 'nssf_number')
        }),
        ('Verification Details', {
            'fields': ('is_verified', 'verified_at', 'verified_by', 'verification_status')
        }),
        ('Documentation', {
            'fields': ('membership_card',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def verification_status(self, obj):
        if obj.is_verified:
            return format_html('<span style="color: green;">✓ Verified</span>')
        else:
            return format_html('<span style="color: orange;">⏳ Pending Verification</span>')
    verification_status.short_description = 'Status'
    
    actions = ['mark_verified', 'mark_unverified']
    
    def mark_verified(self, request, queryset):
        updated = queryset.update(is_verified=True, verified_by=request.user)
        self.message_user(request, f"{updated} NSSF details marked as verified.")
    mark_verified.short_description = "Mark selected as verified"
    
    def mark_unverified(self, request, queryset):
        updated = queryset.update(is_verified=False, verified_by=None, verified_at=None)
        self.message_user(request, f"{updated} NSSF details marked as unverified.")
    mark_unverified.short_description = "Mark selected as unverified"

@admin.register(NSSFReturn)
class NSSFReturnAdmin(admin.ModelAdmin):
    list_display = ('company', 'month_name', 'submitted_on', 'status_badge', 'is_processed', 'is_late')
    list_filter = ('status', 'is_processed', 'month', 'submitted_on')
    search_fields = ('company__name', 'company__nssf_number')
    raw_id_fields = ('company', 'processed_by')
    readonly_fields = ('submitted_on', 'month_name', 'is_late', 'status_badge')
    date_hierarchy = 'submitted_on'
    
    fieldsets = (
        ('Company Information', {
            'fields': ('company', 'month')
        }),
        ('Return Details', {
            'fields': ('return_file', 'submitted_on', 'month_name')
        }),
        ('Processing Status', {
            'fields': ('is_processed', 'status', 'processed_at', 'processed_by', 'status_badge')
        }),
        ('Additional Information', {
            'fields': ('notes', 'is_late'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'approved': 'green',
            'rejected': 'red'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 6px; border-radius: 4px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def is_late(self, obj):
        return obj.is_late
    is_late.boolean = True
    is_late.short_description = 'Late Submission'
    
    actions = ['mark_processed', 'mark_unprocessed', 'approve_returns', 'reject_returns']
    
    def mark_processed(self, request, queryset):
        updated = queryset.update(is_processed=True, processed_by=request.user, status='processing')
        self.message_user(request, f"{updated} returns marked as processed.")
    mark_processed.short_description = "Mark selected as processed"
    
    def mark_unprocessed(self, request, queryset):
        updated = queryset.update(is_processed=False, processed_by=None, processed_at=None, status='pending')
        self.message_user(request, f"{updated} returns marked as unprocessed.")
    mark_unprocessed.short_description = "Mark selected as unprocessed"
    
    def approve_returns(self, request, queryset):
        updated = queryset.update(status='approved', is_processed=True, processed_by=request.user)
        self.message_user(request, f"{updated} returns approved.")
    approve_returns.short_description = "Approve selected returns"
    
    def reject_returns(self, request, queryset):
        updated = queryset.update(status='rejected', is_processed=True, processed_by=request.user)
        self.message_user(request, f"{updated} returns rejected.")
    reject_returns.short_description = "Reject selected returns"