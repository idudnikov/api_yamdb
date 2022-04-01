from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .emailconfirmation import EmailConfirmationViewSet
from api.tokens import TokenViewAPI

app_name = 'api'

router = DefaultRouter()

router.register(r'users', '----', basename='users')
router.register(r'categories', '----', basename='categories')
router.register(r'genres', '----', basename='genres')
router.register(r'titles', '----', basename='titles')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    '----',
    basename='reviews')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    '----',
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewAPI.as_view(), name='token_obtain_pair'),
    path(
        'v1/auth/signup/',
        EmailConfirmationViewSet.as_view(), name='regist_user_conf_email'),
]
