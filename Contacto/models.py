from django.db import models

# Create your models here.

class Contacto(models.Model):
    username = models.CharField(max_length = 30,verbose_name="Nombre de Usuario", default = "")
    titulo = models.CharField(max_length = 100)
    email_from = models.EmailField()
    comentario = models.TextField(blank=True,null=True,default = "")
    def __str__(self):
        return self.titulo