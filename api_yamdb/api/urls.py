from django.urls import path
from api.tokens import TokenViewAPI

from .emailconfirmation import EmailConfirmationViewSet

app_name = 'api'

urlpatterns = [
    path('v1/auth/token/', TokenViewAPI.as_view(), name='token_obtain_pair'),
    path(
        'v1/auth/signup/',
        EmailConfirmationViewSet.as_view(), name='regist_user_conf_email'),
]
