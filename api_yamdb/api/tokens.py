from uuid import uuid4

from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import CustomUser


class TokenSerializer(serializers.ModelSerializer):
    """Class TokenSerializer."""

    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']

    def validate_username(self, value):
        get_object_or_404(CustomUser, username=value)
        return value

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = CustomUser.objects.filter(
            username=username, confirmation_code=confirmation_code
        )
        if not user.exists():
            raise serializers.ValidationError({
                "Wrong username or confirmation code":
                    "Please input correct data."
            })
        return data


class TokenViewAPI(GenericAPIView):
    """Class TokenAPI."""

    serializer_class = TokenSerializer

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = CustomUser.objects.get(
                username=serializer.validated_data['username'],
                confirmation_code=(
                    serializer.validated_data['confirmation_code'])
            )
            token = AccessToken.for_user(user)
            user.confirmation_code = uuid4()
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
