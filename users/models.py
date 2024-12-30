import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy
from .manager import UserManager

class User(AbstractUser, PermissionsMixin):
    first_name = None  # Sobrescribir el campo first_name de AbstractUser
    last_name = None   # Sobrescribir el campo last_name de AbstractUser
    username = None 

    name = models.CharField(
        gettext_lazy('First name'), max_length=30, blank=False, null=False
    )
    lastname = models.CharField(
        gettext_lazy('Last name'), max_length=30, blank=False, null=False
    )
    cellphone = models.CharField(
        gettext_lazy('Cellphone'), max_length=10, blank=True, null=True
    )
    email = models.EmailField(
        gettext_lazy('Email'), max_length=254, unique=True, null=False
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    date_joined = models.DateTimeField(gettext_lazy('Date joined'), auto_now_add=True)
    is_staff = models.BooleanField(gettext_lazy('Staff'), default=False, help_text=gettext_lazy('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(gettext_lazy('Active'), default=False)
    servicio = models.CharField(gettext_lazy('Service'), max_length=30, blank=True, null=True)
    cargo = models.CharField(gettext_lazy('Cargo'), max_length=30, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "lastname"]

    class Meta:
        verbose_name = gettext_lazy('user')
        verbose_name_plural = gettext_lazy('users')

    @property
    def full_name(self):
        return f'{self.name} {self.lastname}'
    
    def get_short_name(self):
        return self.name
    
    def email_user(self, subject, message, from_email=None, **kwargs):

        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def __str__(self):
        return self.name
    


