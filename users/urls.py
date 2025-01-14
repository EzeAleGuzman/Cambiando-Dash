from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("confirmacionregistro/", views.confirmacionregistro, name="confirmacionregistro"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("recover_password/", views.recover_password, name="recover_password"),

]
