from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'lastname', 'cellphone','servicio', 'cargo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),  # Excluir 'date_joined' aquí
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'lastname','servicio', 'cargo','password1', 'password2')
        }),
    )
    list_display = ('email', 'name', 'lastname', 'is_staff')
    search_fields = ('email', 'name', 'lastname')
    ordering = ('email',)

# Registrar el modelo User en el admin
admin.site.register(User, UserAdmin)
