from os import path
from django.conf import settings
from django.db.models.signals import pre_delete
from .models import Ad
from django.dispatch import receiver

@receiver(pre_delete, sender=Ad)
def delete_image_hook(sender, instance, using, **kwargs):
    if instance.image.path != path.join(settings.BASE_DIR, 'media\default.jpg'):
        instance.image.delete(save=False)