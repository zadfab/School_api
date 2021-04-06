
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):

    def _create_user(self,email,password,is_staff,is_superuser,**extrafields):
        if not email:
            raise ValueError("Email can not be set empty")
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_superuser=is_superuser,
                          is_staff=is_staff,
                          last_login =timezone.now(),
                          **extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self,email,password=None,**extrafields):
        return self._create_user(email,password,False,False,**extrafields)

    def create_superuser(self,email,password=None,**extrafields):
        return self._create_user(email,password,True,True,**extrafields)
