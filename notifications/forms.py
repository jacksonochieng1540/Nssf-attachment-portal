from django import forms
from .models import NotificationPreference

class NotificationPreferenceForm(forms.ModelForm):
    class Meta:
        model = NotificationPreference
        fields = [
            'email_enabled', 'push_enabled', 'in_app_enabled', 'digest_frequency',
            'attachment_updates', 'nssf_updates', 'message_notifications', 
            'announcement_notifications'
        ]
        widgets = {
            'digest_frequency': forms.Select(attrs={'class': 'form-control'}),
        }