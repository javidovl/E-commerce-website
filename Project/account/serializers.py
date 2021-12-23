from django.contrib.auth import get_user_model
from rest_framework import routers, serializers, viewsets
import account

from account.models import User

Usermodel=get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usermodel
        fields = '__all__'
