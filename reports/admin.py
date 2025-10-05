# reports/admin.py
from django.contrib import admin
from .models import ReportHistory

@admin.register(ReportHistory)
class ReportHistoryAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'generated_by', 'generated_at', 'download_count')
    list_filter = ('report_type', 'generated_at')
    search_fields = ('generated_by__username',)
    raw_id_fields = ('generated_by',)
    date_hierarchy = 'generated_at'
    readonly_fields = ('generated_at',)