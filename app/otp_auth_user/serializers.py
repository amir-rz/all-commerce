from rest_framework import serializers

from django.contrib.auth import get_user_model

from phonenumber_field.serializerfields import PhoneNumberField


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["id", "phone", "full_name"]
        extra_kwargs = {
            "id": {"read_only": True}
        }

    def create(self, validated_data):
        """ Create and return a new user """
        user = get_user_model().objects.create_user(
            phone=validated_data["phone"],
            full_name=validated_data["full_name"],
        )

        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class RequestVCodeSerializer(serializers.Serializer):
    phone = PhoneNumberField()


class SigninUserSerializer(serializers.Serializer):
    phone = PhoneNumberField()
    verification_code = serializers.CharField()