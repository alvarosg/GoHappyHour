from models import *

def ObtainUserLabel(user):

    fullname=user.get_full_name()
    if fullname!="":
        return fullname
    else:
        return user.username
    