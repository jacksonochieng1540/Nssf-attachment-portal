from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import Company

@receiver(post_save, sender=User)
def create_company_profile(sender, instance, created, **kwargs):
    """Create a company profile when a user's role is set to 'company'"""
    if instance.role == 'company' and not hasattr(instance, 'company'):
        Company.objects.create(
            user=instance,
            name=f"{instance.get_full_name()}'s Company",
            address="Please update company address"
        )