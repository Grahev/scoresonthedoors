# your_app/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from authentication.telegram_utils import send_telegram_message

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        # Send an email notification to your email address
        subject = 'New User Registration'
        message = f'A new user has registered: {instance.username}'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Sender email address
            [settings.NOTIFICATION_EMAIL],  # Recipient email address
            fail_silently=False,
        )

@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        message = f'A new user has registered: {instance.username}'
        response = send_telegram_message(message)
        # Optionally log or handle the response
        print(response)


@receiver(pre_save, sender=User)
def user_status_changed(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = User.objects.get(pk=instance.pk)
            if not old_instance.is_active and instance.is_active:
                # Notify when user status changes to active
                message = f'User account activated: {instance.username}'
                response = send_telegram_message(message)
                # Optionally log or handle the response
                print(response)
        except User.DoesNotExist:
            # If the user does not exist yet (creating), do nothing
            pass