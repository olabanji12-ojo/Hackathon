from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Customer
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        customer = Customer.objects.create(
            user=instance,
            email=instance.email
        )
        print('Customer has been created')
        
        subject = 'Welcome to Emmanuel\'s website'
        message = 'We are glad you could make it!'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [instance.email],
            fail_silently=False
        )


@receiver(post_save, sender=User)
def update_customer(sender, instance, created, **kwargs):
    if not created:
        try:
            customer = instance.customer
            customer.email = instance.email
            customer.save()
            print('Customer has been updated')
        except ObjectDoesNotExist:
            print('Customer instance does not exist for this user')


@receiver(post_delete, sender=Customer)
def delete_user(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
        print('User associated with customer has been deleted')
    except ObjectDoesNotExist:
        print('User instance does not exist for this customer')
