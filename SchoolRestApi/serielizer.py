from rest_framework import serializers
from .models import SchoolUser
from django.contrib.auth.hashers import make_password

class SchoolUserSerializer(serializers.ModelSerializer):
    # date_joined =serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SchoolUser
        fields = "__all__"
        extra_kwargs ={"password":{"write_only":True}}

    def validate_password(self, value: str) -> str:
        """
        Hash value passed by user.

        :param value: password of a user
        :return: a hashed version of the password
        """
        return make_password(value)


class filterUserSerielizer(serializers.ModelSerializer):
    class Meta:
        model = SchoolUser
        fields = ["email","first_name","last_name","type"]