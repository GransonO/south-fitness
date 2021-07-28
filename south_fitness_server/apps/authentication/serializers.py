from rest_framework import serializers
from .models import User, Activation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'first_name', 'last_name', 'is_active']


class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activation
        fields = '__all__'
