from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

from cfehome.serializers import MessageSerializer

User = get_user_model()


class UserExistsMessageSerializer(MessageSerializer):
    exists = serializers.BooleanField()


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()


class TokenVerifyResponseSerializer(serializers.Serializer):
    pass


class RegisterAccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "is_staff",
            "is_active",
            "is_superuser",
            "password",
            "password2",
        )

        read_only_fields = (
            "id",
            "email_verified",
            "is_staff",
            "is_active",
            "is_superuser",
        )

    def create(self, validated_data):
        del validated_data["password2"]

        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, data):
        password = data["password"]
        errors = dict()

        if data["password"] != data["password2"]:
            errors["password"] = ["The two password fields didn’t match."]

        newData = data.copy()
        newData.pop("password2")

        account = User(**newData)
        try:
            validate_password(password, user=account)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "email_verified",
            "is_staff",
            "is_active",
            "is_superuser",
        )

        read_only_fields = (
            "id",
            "email",
            "email_verified",
            "is_staff",
            "is_active",
            "is_superuser",
        )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "name",
            "permissions",
        )


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = (
            "id",
            "name",
            "codename",
            "content_type",
        )


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate(self, data):
        errors = dict()

        if data["old_password"] == data["new_password"]:
            errors["new_password"] = [
                "New password must be different from old password"
            ]

        if data["new_password"] != data["new_password2"]:
            errors["new_password"] = ["The two password fields didn’t match."]

        try:
            validate_password(password=data["new_password"])
        except exceptions.ValidationError as e:
            errors["new_password"] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return data


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
