from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import (api_view,permission_classes)
from rest_framework import status
from .serielizer import  *
from rest_framework.viewsets import ModelViewSet
from .models import *
from .authentication import ExampleAuthentication
from rest_framework.permissions import IsAuthenticated
from .decorate import allowed_user
# Create your views here.


@api_view(['GET'])
def welcome(request):
    return Response({"data":"Sucessfully implemented"},status =status.HTTP_202_ACCEPTED )

@api_view(["POST"])
@allowed_user(allowed_roles=["Admin"])
def user_signup(request):
    """
    Url for Admin.(Admin is allowed to add any user (Admin,Teacher,Student))
    To add any type of user by admin only.
    #Json Structure:
        {"email":"example@gmail.com","password":"12345678","type":"Student","first_name":"Zaid","last_name":"fab"}
    """
    data = request.data

    try:
        email = data["email"]
        password = data["password"]
        user_type = data["type"]
        first_name = data["first_name"]
        last_name =  data["last_name"]
    except:
        return Response("Parameter missing",status=status.HTTP_404_NOT_FOUND)
    seriealize = SchoolUserSerializer(data = data)
    if seriealize.is_valid():
        seriealize.save()
        returning_data = seriealize.data
    else:
        returning_data = seriealize.errors
    return Response(returning_data)


class Admin(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [ExampleAuthentication]
    serializer_class = filterUserSerielizer
    queryset = SchoolUser.objects.all()
    lookup_field = "email"

@api_view(["POST"])
@permission_classes([IsAuthenticated])
@allowed_user(allowed_roles=["Student","Teacher","Admin"])
def student(request):
    """
    To view a particular user info.
    Url for student.(Student can only view its own information.)
    """

    try:
        db_obj = SchoolUser.objects.get(email=request.user)
        data =  SchoolUserSerializer(db_obj).data
    except:
        return Response({"Error":"Email not found"},status=status.HTTP_404_NOT_FOUND)

    return Response(data,status=status.HTTP_202_ACCEPTED)

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
@allowed_user(allowed_roles=["Teacher","Admin"])
def teacher(request):
    """
    ###Url for Teacher.
    ***Teacher can view all the student and can add new student.***

    ##Json structure
    ######{"email":"example@gmail.com","password":"12345678","first_name":"Zaid","last_name":"fab"}
    """

    if request.method == "GET":
        db_obj  = SchoolUser.objects.filter(type="Student")
        data = SchoolUserSerializer(db_obj,many=True)
        return Response(data.data,status=status.HTTP_202_ACCEPTED)

    elif request.method =="POST":
        data = request.data
        data["type"] = "Student"
        print(data)
        storing_data = SchoolUserSerializer(data=data)
        if storing_data.is_valid():
            storing_data.save()
            return Response(storing_data.data)
           # return Response("lvl 2  under construction",storing_data.errors)
        else:
            return Response(f"lvl 2  under construction {storing_data.errors}")

