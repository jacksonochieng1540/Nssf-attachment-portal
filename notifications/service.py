# notifications/services.py
from django.db import transaction
from .models import Notification, NotificationPreference

class NotificationService:
    @staticmethod
    def send_notification(user, notification_type, title, message, link=None, related_object=None):
        """
        Send a notification to a user
        """
        # Check user preferences
        preference, created = NotificationPreference.objects.get_or_create(user=user)
        
        # Check if user wants this type of notification
        if not NotificationService._should_send_notification(preference, notification_type):
            return None
        
        # Create notification
        notification = Notification.create_notification(
            user=user,
            notification_type=notification_type,
            title=title,
            message=message,
            link=link,
            related_object=related_object
        )
        
        # TODO: Add email and push notifications here
        if preference.email_enabled:
            NotificationService._send_email_notification(notification)
        
        if preference.push_enabled:
            NotificationService._send_push_notification(notification)
        
        return notification
    
    @staticmethod
    def _should_send_notification(preference, notification_type):
        """Check if user wants to receive this type of notification"""
        mapping = {
            'attachment_approved': preference.attachment_updates,
            'attachment_rejected': preference.attachment_updates,
            'nssf_verified': preference.nssf_updates,
            'return_processed': preference.nssf_updates,
            'message': preference.message_notifications,
            'announcement': preference.announcement_notifications,
            'alert': True,  # Always send alerts
            'reminder': True,  # Always send reminders
        }
        return mapping.get(notification_type, True)
    
    @staticmethod
    def _send_email_notification(notification):
        """Send email notification (to be implemented)"""
        # TODO: Implement email sending
        pass
    
    @staticmethod
    def _send_push_notification(notification):
        """Send push notification (to be implemented)"""
        # TODO: Implement push notifications
        pass
    
    @staticmethod
    def notify_attachment_approved(attachment):
        """Notify student when attachment is approved"""
        from notifications.services import NotificationService
        
        NotificationService.send_notification(
            user=attachment.student.user,
            notification_type='attachment_approved',
            title='Attachment Approved',
            message=f'Your attachment at {attachment.company.name} has been approved!',
            link=f'/attachments/{attachment.pk}/'
        )
    
    @staticmethod
    def notify_attachment_rejected(attachment):
        """Notify student when attachment is rejected"""
        from notifications.services import NotificationService
        
        NotificationService.send_notification(
            user=attachment.student.user,
            notification_type='attachment_rejected',
            title='Attachment Rejected',
            message=f'Your attachment at {attachment.company.name} was rejected.',
            link=f'/attachments/{attachment.pk}/'
        )
    
    @staticmethod
    def notify_nssf_verified(student_profile):
        """Notify student when NSSF is verified"""
        from notifications.services import NotificationService
        
        NotificationService.send_notification(
            user=student_profile.user,
            notification_type='nssf_verified',
            title='NSSF Verified',
            message='Your NSSF details have been verified successfully!',
            link='/nssf/details/'
        )