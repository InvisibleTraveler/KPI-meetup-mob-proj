from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

from accounts.models import Visitor, User, Lector, USER_TYPE, Rate

USER_CLASS = {
    USER_TYPE.VISITOR: Visitor,
    USER_TYPE.LECTOR: Lector,
}


# TODO decompose
class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=128, required=True, style={"input_type": "username"})
    password = serializers.CharField(max_length=128, required=True, style={"input_type": "password"})
    email = serializers.EmailField(required=True)
    user_type = serializers.ChoiceField(choices=USER_TYPE, required=True)

    def validate_password(self, password):
        try:
            validate_password(password)
        except DjangoValidationError as e:
            raise ValidationError(detail=e.messages)
        return password

    def create(self, validated_data):
        try:
            user = User.objects.create_user(
                username=validated_data["username"],
                email=validated_data["email"],
                password=validated_data["password"],
            )
            USER_CLASS[validated_data.get("user_type")].objects.create(user=user)
        except IntegrityError:
            raise ValidationError({"username": "User with this username is already exists"})
        return user

    def update(self, instance, validated_data):
        assert False, "Could not use this serializer for update"


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "location",
        )
        read_only_fields = ('username', 'email',)


class LectorSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer(read_only=True)

    class Meta:
        model = Lector
        fields = (
            "id",
            "user",
            "description",
            "rate_count",
            "rate_summary",
            "rate",
        )
        read_only_fields = ('rate_count', 'rate_summary', 'rate')


class VisitorSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer(read_only=True)

    class Meta:
        model = Visitor
        fields = (
            "id",
            "user",
        )


class CreateRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            "id",
            "visitor",
            "lector",
            "rate",
            "comment",
        )


class ReadUpdateRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = (
            "rate",
            "comment",
        )

    def create(self, validated_data):
        assert False, "Can't create rate"
