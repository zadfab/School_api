from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_view
from rest_framework.routers import  DefaultRouter

routers =  DefaultRouter()
routers.register("admin",views.Admin)


urlpatterns = [
    path('', include(routers.urls)),
    path('', views.welcome,name = "welcome"),
    path('user_signup', views.user_signup,name = "user_signup"),
    path('student', views.student,name = "student"),
    path('teacher', views.teacher,name = "teacher"),
    # path('reset_password',auth_view.PasswordResetView.as_view()),
    # path('reset_password_sent',auth_view.PasswordResetDoneView.as_view()),
    # path('reset/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view()),
    # path('reset_password_complete',auth_view.PasswordResetCompleteView.as_view()),

]
