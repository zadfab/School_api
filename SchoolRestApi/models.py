from django.db import models
from django.contrib.auth.models import  AbstractUser
from .Manager import UserManager
from django.dispatch import receiver
from django.db.models.signals import  post_save
from django.contrib.auth.models import Group
# Create your models here.

class SchoolUser(AbstractUser):
    user_type = (("Admin","Admin"),
                 ("Student","Student"),
                 ("Teacher","Teacher"))
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30,blank=True,null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=20,choices=user_type)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['type']


    class Meta:
        db_table = "SchoolUsers"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name

@receiver(post_save,sender = SchoolUser)
def set_group(sender,instance,created,*args,**kwargs):

    if created:
        group,creat = Group.objects.get_or_create(name=instance.type)
        group.user_set.add(instance)


