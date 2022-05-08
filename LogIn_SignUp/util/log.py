from LogIn_SignUp.models import User

def aut_log(ip):
    # Busca en todos los usuarios
    for user in User.objects.all():
        # Si la direccion ip coincide
        if ip == user.ip_address:
            # Ve a ver si es su ultimo login
            if user.last_login:
                # Si no esta logueado devuelvele -1 (Inicio-Sesion)
                if not user.is_logged:
                    return -1
                # Si esta logueado devuelvele el objeto (landing_page)
                else:
                    return user
    # Si todo falla devuelvele None y asi se va pal registro
    return None