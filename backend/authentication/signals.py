from django.db.models.signals import post_save
from django.dispatch import receiver
from  core.models  import Landlord, Agent, Tenant
from .models import CustomUser 

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'landlord':
            Landlord.objects.create(user=instance, name=instance.email)
        elif instance.user_type == 'agent':
            Agent.objects.create(user=instance, name=instance.email)

        elif instance.user_type == 'tenant':
            Tenant.objects.create(user=instance, name=instance.email, landlord=None)
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 'landlord':
        instance.landlord_profile.save()
    elif instance.user_type == 'agent':
        instance.agent_profile.save()
    elif instance.user_type == 'tenant':
        instance.tenant_profile.save()



