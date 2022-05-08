from django.shortcuts import render
from LogIn_SignUp.util.log import aut_log
from django.http import HttpResponseRedirect
from LogIn_SignUp.views import get_user_logged_first_char
# Create your views here.

def init(request):
    var_aut_log = aut_log(request.META["REMOTE_ADDR"])
    if var_aut_log == -1:
        return HttpResponseRedirect("/Inicio-Sesion/",{"initial_username":get_user_logged_first_char(request)})
    elif var_aut_log is None:
        return HttpResponseRedirect("/registro/",{"initial_username":get_user_logged_first_char(request)})
    else:
        return render(request,"index.html",{"initial_username":get_user_logged_first_char(request)})
