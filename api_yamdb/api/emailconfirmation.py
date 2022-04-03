from uuid import uuid4

from django.core.mail import EmailMessage
from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from users.models import CustomUser


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """Class CustomUserSerializer."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {"Wrong username": "User 'me' can not be created."}
            )
        return data


class EmailConfirmationViewSet(CreateModelMixin, GenericAPIView):
    """Class EmailConfirmationViewSet."""

    serializer_class = CreateCustomUserSerializer

    def post(self, request):
        serializer = CreateCustomUserSerializer(data=request.data)
        if serializer.is_valid():
            confirmation_code = uuid4()
            # send email
            email = EmailMessage(
                'Hello',
                f'This is your confirmation code: {confirmation_code}',
                'YaMDB@yandex.ru',
                [serializer.validated_data.get('email')]
            )
            email.send()
            serializer.save()
            CustomUser.objects.filter(
                username=serializer.validated_data.get('username')
            ).update(confirmation_code=confirmation_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
