from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name"
        )
        optional_fields = ("first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True},
        }


class UserUpdateSerializer(UserSerializer):
    email = serializers.CharField(required=False, min_length=1)
    password = serializers.CharField(
        write_only=True, required=False, style={"input_type": "password"}, min_length=1
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name"
        )
        optional_fields = ("email", "first_name", "last_name", "password")
        extra_kwargs = {
            "id": {"read_only": True},
        }
