from django.urls import path, include
from .tokens import TokenViewAPI
from .emailconfirmation import EmailConfirmationViewSet

app_name = "api"


urlpatterns = [
    path('api/v1/auth/token/', TokenViewAPI.as_view(), name='token_obtain_pair'),
    path(
        'api/v1/auth/signup/',
        EmailConfirmationViewSet.as_view(), name='regist_user_conf_email'),
    #path('api/v1/users/me/',),

]
