from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from LogIn_SignUp.util.log import aut_log
from LogIn_SignUp.views import get_user_logged_first_char
from Contacto.models import Contacto
from LogIn_SignUp.models import User
# Create your views here.

def contacto(request):
    if request.method =="POST":
        username = ""
        for user in User.objects.all():
            if user.ip_address == request.META["REMOTE_ADDR"]:
                if user.last_login:
                    if user.is_logged:
                        username = user.username
                    else:
                        return HttpResponseRedirect("/Inicio-Sesion")
        email_from = request.POST["email_from"]
        comentario = request.POST["comentario"]
        titulo = request.POST["titulo"]
        if len(titulo)>70:
            return HttpResponseRedirect("Contacto/")
        contacto = Contacto(username =username,email_from = email_from,comentario = comentario, titulo = titulo)
        contacto.save()
        return HttpResponse("""
        <html>
        <body>
            <h1>Gracias por su comentario, gracias Click 
            <a href = '/' style ='cursor:pointer; color:blue'>aqui</a> para volver al inicio</h1>
        </body>
        </html>
        """)
    else:
        var_aut_log = aut_log(request.META["REMOTE_ADDR"])
        if var_aut_log == -1:
            return HttpResponseRedirect("/Inicio-Sesion/",{"initial_username":get_user_logged_first_char(request)})
        elif var_aut_log is None:
            return HttpResponseRedirect("/registro/",{"initial_username":get_user_logged_first_char(request)})
        else:
            return render(request,"Contacto.html")