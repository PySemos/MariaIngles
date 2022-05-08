from django.contrib import admin
from Contacto.models import Contacto
# Register your models here.
class ContactoAdmin(admin.ModelAdmin):
    list_display = ("username","email_from","titulo")
    search_fields = ("email_from","titulo")

admin.site.register(Contacto,ContactoAdmin)