
class CodeUserAutenticate:
    OK = 0
    USERNAME_EQUAL = 1
    EMAIL_EQUAL = -1

class CodeUserAutenticateLogIn:
    OK = 0
    BADPASSWORD = 1
    BADUSERNAME = -1

# autentifica el usuario por el usuario e email
def autenticate_user_sign_up(username_email,Users):
    for u in Users:
        if username_email[0] == u.username:
            return CodeUserAutenticate.USERNAME_EQUAL
        elif username_email[1] == u.email:
            return CodeUserAutenticate.EMAIL_EQUAL
    return CodeUserAutenticate.OK

def autenticate_user_log_in(username,password,Users):
    for user in Users:
        if username == user.username and password == user.password:
            return user
        elif username == user.username and password!= user.password:
            return CodeUserAutenticateLogIn.BADPASSWORD
    return CodeUserAutenticateLogIn.BADUSERNAME





