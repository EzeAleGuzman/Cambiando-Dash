from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import User

@receiver(post_save, sender=User)
def send_admin_notification_on_update(sender, instance, created, **kwargs):
    if created:
        subject = 'Nuevo usuario creado'
    else:
        subject = 'Datos Usuario actualizado'

    # Crear el contenido del correo en formato HTML
    message = render_to_string('emails/user_update_notification.html', {
        'name': instance.name,
        'lastname': instance.lastname,
        'email': instance.email,
        'cellphone': instance.cellphone,
        'servicio': instance.servicio,
        'cargo': instance.cargo,
        'action': 'creado' if created else 'actualizado',  # Especifica si es creación o actualización
    })

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [admin[1] for admin in settings.ADMINS],  # Extraemos los correos de la lista ADMINS
        fail_silently=False,
        html_message=message  # Especificar que el contenido es HTML
    )