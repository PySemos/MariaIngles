from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=30, verbose_name="Nombre de usuario")
    last_name = models.CharField(max_length=30,verbose_name="Apellido paterno",blank=True, null=True,default = "")    
    password = models.CharField(max_length=40, verbose_name="Contraseña")
    email = models.EmailField(verbose_name = "Correo electrónico")
    age = models.IntegerField(blank=True, null=True, verbose_name="Edad")
    ci = models.CharField(max_length=30,default="")
    ip_address = models.CharField(max_length = 20, default = "")
    is_logged = models.BooleanField(default = False)
    last_login = models.BooleanField(default = False)