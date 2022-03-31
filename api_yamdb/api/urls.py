from django.urls import path, include
from .tokens import TokenViewAPI
from .emailconfirmation import EmailConfirmationViewSet

app_name = "api"

urlpatterns = [
    path('v1/auth/token/', TokenViewAPI.as_view(), name='token_obtain_pair'),
    path('v1/auth/signup/', EmailConfirmationViewSet, name='register_user'),
    # path('/api/v1/users/me/', ),
]
