from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import send_mail
from .models import User
from django.utils.html import strip_tags

@receiver(pre_save, sender=User)
def save_old_user_data(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_user = User.objects.get(pk=instance.pk)
        except User.DoesNotExist:
            instance._old_user = None

@receiver(post_save, sender=User)
def send_admin_notification_on_update(sender, instance, created, **kwargs):
    if created:
        subject = 'Nuevo usuario creado'
        send_notification = True
    else:
        old_user = getattr(instance, '_old_user', None)
        if old_user:
            # Compara los valores anteriores con los valores actuales
            send_notification = (
                old_user.name != instance.name or
                old_user.lastname != instance.lastname or
                old_user.email != instance.email or
                old_user.cellphone != instance.cellphone or
                old_user.servicio != instance.servicio or
                old_user.cargo != instance.cargo
            )
        else:
            send_notification = False

    if send_notification:
        # Crear el contenido del correo en formato HTML
        html_message = render_to_string('emails/user_update_notification.html', {
            'name': instance.name,
            'lastname': instance.lastname,
            'email': instance.email,
            'cellphone': instance.cellphone,
            'servicio': instance.servicio,
            'cargo': instance.cargo,
        })

        plain_message = strip_tags(html_message)
        from_email = 'saluddigitalona@gmail.com'
        to = ['saluddigitalona@gmail.com']

        send_mail(
            subject,
            plain_message,
            from_email,
            to,
            fail_silently=False,
            html_message=html_message,
         )

