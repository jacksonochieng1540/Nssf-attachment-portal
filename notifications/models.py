# notifications/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('attachment_approved', 'Attachment Approved'),
        ('attachment_rejected', 'Attachment Rejected'),
        ('nssf_verified', 'NSSF Verified'),
        ('return_processed', 'Return Processed'),
        ('message', 'Message'),
        ('alert', 'Alert'),
        ('announcement', 'Announcement'),
        ('reminder', 'Reminder'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=500, blank=True, null=True)
    related_object_id = models.PositiveIntegerField(blank=True, null=True)
    related_content_type = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.title}"
    
    def mark_as_read(self):
        self.is_read = True
        self.save()
    
    def get_absolute_url(self):
        if self.link:
            return self.link
        return reverse('notifications:list')
    
    @classmethod
    def create_notification(cls, user, notification_type, title, message, link=None, 
                          related_object=None):
        notification = cls(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link
        )
        
        if related_object:
            notification.related_object_id = related_object.id
            notification.related_content_type = related_object.__class__.__name__
        
        notification.save()
        return notification

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')
    email_enabled = models.BooleanField(default=True)
    push_enabled = models.BooleanField(default=True)
    in_app_enabled = models.BooleanField(default=True)
    digest_frequency = models.CharField(max_length=10, choices=[
        ('immediate', 'Immediately'),
        ('daily', 'Daily Digest'),
        ('weekly', 'Weekly Digest')
    ], default='immediate')
    
    # Notification type preferences
    attachment_updates = models.BooleanField(default=True)
    nssf_updates = models.BooleanField(default=True)
    message_notifications = models.BooleanField(default=True)
    announcement_notifications = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"