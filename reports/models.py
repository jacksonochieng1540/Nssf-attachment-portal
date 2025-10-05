# reports/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ReportHistory(models.Model):
    REPORT_TYPES = (
        ('students', 'Students Report'),
        ('companies', 'Companies Report'),
        ('attachments', 'Attachments Report'),
        ('nssf_returns', 'NSSF Returns Report'),
    )
    
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    generated_at = models.DateTimeField(auto_now_add=True)
    parameters = models.JSONField(default=dict)  # Store filter parameters
    download_count = models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Report Histories"
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"{self.get_report_type_display()} - {self.generated_at.strftime('%Y-%m-%d %H:%M')}"