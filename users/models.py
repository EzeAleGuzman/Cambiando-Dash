import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy
from manager import UserManager

class User(AbstractUser, PermissionsMixin):
    name = models.CharField(
        gettext_lazy('First name'), max_length=30, blank=False, null=False
    )
    Lastname = models.CharField(
        gettext_lazy('Last name'), max_length=30, blank=False, null=False
    )
    cellphone = models.CharField(
        gettext_lazy('Cellphone'), max_length=10, blank=False, null=False
    )
    email = models.EmailField(
        gettext_lazy('Email'), max_length=254, unique=True, null=False
    )
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    date_joined = models.DateTimeField(gettext_lazy('Date joined'), auto_now_add=True)
    is_staff = models.BooleanField(gettext_lazy('Staff'), default=False, help_text=gettext_lazy('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(gettext_lazy('Active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'Lastname']

    class Meta:
        verbose_name = gettext_lazy('User')
        verbose_name_plural = gettext_lazy('Users')

    @property
    def full_name(self):
        return f'{self.name} {self.Lastname}'
    
    def get_short_name(self):
        return self.name
    
    def email_user(self, subject, message, from_email=None, **kwargs):

        send_mail(subject, message, from_email, [self.email], **kwargs)
    
    def __str__(self):
        return self.name
    


