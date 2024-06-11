from rest_framework import serializers

from .models import User, Seller


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "groups", "user_permissions")


class UpdateUserSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        serializer = UserSerializer(instance)
        return serializer.data

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'password', 'id'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'
