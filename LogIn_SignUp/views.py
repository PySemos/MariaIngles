from wsgiref.util import request_uri
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from LogIn_SignUp.models import User
from LogIn_SignUp.util import autenticate
from LogIn_SignUp.util.user import UserClass
from LogIn_SignUp.util.log import aut_log
# Create your views here.
email_username_from_change_password = 0
def get_user_logged_first_char(request_obj):
    ip = request_obj.META["REMOTE_ADDR"]
    for user in User.objects.all():
        if user.ip_address == ip and user.last_login and user.is_logged:
            return user.username[0].upper()

@csrf_exempt
def sign_up(request,username_ok = True, email_ok = True):
    if request.method == "POST" and username_ok and email_ok:
        # Obtener datos de Usuario
        usuario = UserClass(
            request.POST["username"],
            request.POST["password"],
            request.POST["email"],
            request.POST["age"],
            str(request.POST["ID"]),
            request.POST["lastname"],
            )
        users_db = tuple(User.objects.all())
        if usuario.username and usuario.password and usuario.email and usuario.age:
            # El usuario introdujo datos validos
            if autenticate.autenticate_user_sign_up([usuario.username,usuario.email],users_db) == autenticate.CodeUserAutenticate.OK:
                usuario_creado = User(
                    username = usuario.username,
                    password = usuario.password,
                    email = usuario.email,
                    age = usuario.age,
                    ci = usuario.ci,
                    last_name = usuario.last_name,
                    ip_address = request.META["REMOTE_ADDR"],
                    is_logged = True,
                    last_login = True,
                    )
                # Poner last_login a las demas cuenas a False
                for user in users_db:
                    if user.ip_address == usuario_creado.ip_address:
                        user.last_login = False
                        user.is_logged = False
                        user.save()
                        
                usuario_creado.save()
                return HttpResponseRedirect("/")
            # El usuario introdujo un nombre de usuario ya tomado por otro usuario
            elif autenticate.autenticate_user_sign_up([usuario.username,usuario.email],users_db) == autenticate.CodeUserAutenticate.USERNAME_EQUAL:
                return sign_up(request,username_ok=False,email_ok=True)
            # O un email ya tomado en otra cuenta
            elif autenticate.autenticate_user_sign_up([usuario.username,usuario.email],users_db) == autenticate.CodeUserAutenticate.EMAIL_EQUAL:
                return sign_up(request,username_ok=True,email_ok=False)
    else:
        return render(request,"sign_up.html",{"username_ok":username_ok,"email_ok":email_ok,"initial_username":get_user_logged_first_char(request)})

@csrf_exempt
def log_in(request,username_ok = True,password_ok = True,temp = True):
    direccion_ip =request.META["REMOTE_ADDR"]
    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["psw"]
        #RENDERIZA
        if not username_ok:
            return render(request,"log_in.html", {"username_ok":False, "password_ok":True})
        if not password_ok:
            return render(request,"log_in.html", {"username_ok":True, "password_ok":False})
        
        #USERNAME MALO
        if autenticate.autenticate_user_log_in(username,password,User.objects.all()) == autenticate.CodeUserAutenticateLogIn.BADUSERNAME:
            return log_in(request,username_ok=False,password_ok=True)
        # CONTRASENIA MALA
        if autenticate.autenticate_user_log_in(username,password,User.objects.all()) == autenticate.CodeUserAutenticateLogIn.BADPASSWORD:
            return log_in(request,username_ok=True,password_ok=False)
        # OK
        if autenticate.autenticate_user_log_in(username,password,User.objects.all()):
            var_temp = autenticate.autenticate_user_log_in(username,password,User.objects.all())
            var_temp.ip_address = direccion_ip
            var_temp.last_login = True
            var_temp.is_logged=True
            for user in User.objects.all():
                if user.ip_address == var_temp.ip_address:
                    user.last_login = False
                    user.is_logged = False
                    user.save()
            var_temp.save()
            return HttpResponseRedirect("/")
    else:
        return render(request,"log_in.html",{"username_ok":True, "password_ok":True,"initial_username":get_user_logged_first_char(request)})


def log_out(request):
    ip  = request.META["REMOTE_ADDR"]
    # Buscar los usuarios registrados con esta IP, luego ver el de el last_login, ponerle el 
    # campo is_logged a ese usuario a False
    for user in User.objects.all():
        if user.ip_address == ip and user.last_login:
            user.is_logged = False
            user.save()
            return HttpResponseRedirect("/Inicio-Sesion")
    return HttpResponse("<center><h1 style = 'color:red;'>Ha ocurrido un error con la salida de sesion</h1><br><a href = '/'>Click aqui para volver al Inicio</a></center>")

def account_info(request):
    ip = request.META["REMOTE_ADDR"]
    for user in User.objects.all():
        if user.ip_address == ip and user.last_login:
            if user.is_logged:
                return render(request,"info_account.html",{
                    "username":user.username,
                    "email":user.email,
                    "apellido":user.last_name,
                    "id":user.ci,
                    "age":user.age,
                    "initial_username":get_user_logged_first_char(request_obj=request)
                })
            else:
                return HttpResponseRedirect("/Inicio-Sesion")
    return HttpResponseRedirect("/registro")
@csrf_exempt
def forgot_password(request):
    if request.method == "POST":
        ip = request.META["REMOTE_ADDR"]
        global email_username_from_change_password
        email_username_from_change_password = request.POST["test_email_username"]
        for user in User.objects.all():
            if ip == user.ip_address:
                if email_username_from_change_password == user.username or email_username_from_change_password == user.email:
                    return render(request,"CambiarContrasenia.html",{"initial_username":get_user_logged_first_char(request)})
        return render(request,"olvidar_contrasenia.html",{"initial_username":get_user_logged_first_char(request),"wrong_aut":False})            

    else:
        var_aut_log = aut_log(request.META["REMOTE_ADDR"])
        if var_aut_log is None:
            return HttpResponseRedirect("/registro/")
        else:
            return render(request,"olvidar_contrasenia.html",{"initial_username":get_user_logged_first_char(request),"wrong_aut":True})
@csrf_exempt
def change_password(request):
    if request.method == "POST":
        global email_username_from_change_password
        ip = request.META["REMOTE_ADDR"]
        if email_username_from_change_password!=0:
            new_password = request.POST["change_password"]
            new_password_again = request.POST["change_password_again"]
            if new_password == new_password_again:
                for user in User.objects.all():
                    if ip == user.ip_address:
                        if email_username_from_change_password == user.username or email_username_from_change_password == user.email:
                            user.password = new_password
                            user.save()
                return HttpResponseRedirect("/")
            else:
                return render(request,"CambiarContrasenia.html",{"initial_username":get_user_logged_first_char(request),"wrong_password_again":True})
        else:
            return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")

def eliminar_usuarios(request):
    for i in User.objects.all():
        i.delete()
    return HttpResponse("<h1>Todos los users han sido eliminados</h1>")