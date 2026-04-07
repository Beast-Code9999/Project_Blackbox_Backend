from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    """
    validates and deserializers regsitration data from Flutter
    Never returned in any response for security
    """

    class Meta:
        model = User
        # fields accepeted in registration request
        fields = ['email', 'password', 'name']

    def create(self, validated_data):
        """
        Override create() because we can't just do User(**data).save()
        create_user() will handle password hashing
        """
        return User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            name = validated_data['name']
        )

class UserSerializer(serializers.ModelSerializer):
    """
    shapes the user data returned in reponse 
    never expose password
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'name']