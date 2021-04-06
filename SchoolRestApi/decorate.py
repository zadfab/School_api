from .models import SchoolUser
from django.contrib.auth.models import Group
from rest_framework.response import  Response


def allowed_user(allowed_roles=[]):
    def decore(view_func):
        def wrapper_func(request,*args,**kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group in allowed_roles:
                  return  view_func(request,*args,**kwargs)
            else:
                return Response("Your are not authorize to view this page")
        return wrapper_func
    return  decore

