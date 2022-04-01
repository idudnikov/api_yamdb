from django.core.mail import EmailMessage
from rest_framework import serializers
from rest_framework import status, viewsets
from rest_framework.response import Response
from uuid import uuid4

from users.models import CustomUser


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """Class CustomUserSerializer."""

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)


class EmailConfirmationViewSet(viewsets.ModelViewSet):
    """"Class EmailConfirmationViewSet."""

    queryset = CustomUser.objects.all()
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
