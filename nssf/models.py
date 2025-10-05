# nssf/models.py
from django.db import models
from django.core.validators import FileExtensionValidator
from attachments.models import StudentProfile, Company

class NSSFDetail(models.Model):
    student = models.OneToOneField(
        StudentProfile, 
        on_delete=models.CASCADE,
        related_name='nssf_details'
    )
    nssf_number = models.CharField(
        max_length=50, 
        unique=True,
        verbose_name='NSSF Number'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Verified Status'
    )
    membership_card = models.FileField(
        upload_to='nssf_cards/%Y/%m/%d/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])],
        blank=True,
        null=True,
        verbose_name='Membership Card'
    )
    verified_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Verification Date'
    )
    verified_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='verified_nssf_details',
        verbose_name='Verified By'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'NSSF Detail'
        verbose_name_plural = 'NSSF Details'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"NSSF Details for {self.student}"
    
    def save(self, *args, **kwargs):
        # If verification status changes to True, set verification timestamp
        if self.is_verified and not self.verified_at:
            from django.utils import timezone
            self.verified_at = timezone.now()
        elif not self.is_verified:
            self.verified_at = None
            self.verified_by = None
        
        super().save(*args, **kwargs)

class NSSFReturn(models.Model):
    RETURN_STATUS = (
        ('pending', 'Pending Review'),
        ('processing', 'Processing'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    company = models.ForeignKey(
        Company, 
        on_delete=models.CASCADE,
        related_name='nssf_returns'
    )
    month = models.DateField(verbose_name='Return Month')
    submitted_on = models.DateTimeField(auto_now_add=True, verbose_name='Submission Date')
    return_file = models.FileField(
        upload_to='nssf_returns/%Y/%m/%d/',
        validators=[FileExtensionValidator(['pdf', 'xlsx', 'xls', 'csv'])],
        verbose_name='Return File'
    )
    is_processed = models.BooleanField(
        default=False,
        verbose_name='Processing Status'
    )
    status = models.CharField(
        max_length=20,
        choices=RETURN_STATUS,
        default='pending',
        verbose_name='Return Status'
    )
    processed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Processing Date'
    )
    processed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='processed_returns',
        verbose_name='Processed By'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Admin Notes'
    )
    
    class Meta:
        verbose_name = 'NSSF Return'
        verbose_name_plural = 'NSSF Returns'
        ordering = ['-submitted_on']
        unique_together = ['company', 'month']  # Prevent duplicate returns for same month
    
    def __str__(self):
        return f"NSSF Return for {self.company} - {self.month.strftime('%B %Y')}"
    
    @property
    def month_name(self):
        """Return the month name for display purposes"""
        return self.month.strftime('%B %Y')
    
    @property
    def is_late(self):
        """Check if the return was submitted late (after the 15th of the following month)"""
        from datetime import date, timedelta
        due_date = date(self.month.year, self.month.month, 15) + timedelta(days=30)
        return self.submitted_on.date() > due_date
    
    def save(self, *args, **kwargs):
        # If processing status changes, update timestamps
        if self.is_processed and not self.processed_at:
            from django.utils import timezone
            self.processed_at = timezone.now()
        elif not self.is_processed:
            self.processed_at = None
            self.processed_by = None
        
        super().save(*args, **kwargs)