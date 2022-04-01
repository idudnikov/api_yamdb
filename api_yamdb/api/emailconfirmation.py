from django.core.mail import EmailMessage
from rest_framework import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from uuid import uuid4

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
            # add confirmation code to CustomUser model
            CustomUser.objects.filter(
                username=serializer.validated_data.get('username')
            ).update(confirmation_code=confirmation_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#{
# user2   "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQ4NzkwODQzLCJpYXQiOjE2NDg3OTA1NDMsImp0aSI6ImFhOWMyZDY3YzBjMzRhNTc5ODgzNDc5OTM5Y2E1YjI3IiwidXNlcl9pZCI6MTA3fQ.Xs0nk-CqNMTTVUfTa68tpOGe6goUty38W3qQ_x3BMjo"
#}
