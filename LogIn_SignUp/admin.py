from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email","age","ci")
    search_fields = ("username","age")

admin.site.register(User,UserAdmin)