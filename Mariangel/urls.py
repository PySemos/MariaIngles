"""Mariangel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from LogIn_SignUp.views import sign_up,eliminar_usuarios,log_in,log_out,account_info,forgot_password,change_password
from landing_page.views import init
from Contacto.views import contacto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',init),
    path('registro/',sign_up),
    path('Inicio-Sesion/',log_in),
    path("eliminarUsers/",eliminar_usuarios),
    path("Salir-Sesion/",log_out),
    path("info/myaccount",account_info),
    path("OlvidarContrasenia/",forgot_password),
    path("cambio_contrasenia/",change_password),
    path("Contacto/",contacto)
]
