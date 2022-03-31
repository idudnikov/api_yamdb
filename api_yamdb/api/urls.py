from django.urls import path, include
from .tokens import TokenViewAPI
from .emailconfirmation import CustomUserViewSet

app_name = "api"

urlpatterns = [
    path('/api/v1/auth/token/', TokenViewAPI.as_view(),
         name='token_obtain_pair'),
    path('/api/v1/auth/signup/', CustomUserViewSet, name='register_user'),
    # path('/api/v1/users/me/', ),
]
