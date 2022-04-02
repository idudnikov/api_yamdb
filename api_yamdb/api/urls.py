from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .emailconfirmation import EmailConfirmationViewSet
from .views import CommentViewSet, ReviewViewSet
from api.tokens import TokenViewAPI

app_name = 'api'

router = DefaultRouter()

router.register(r'users', CommentViewSet, basename='users')
router.register(r'categories', CommentViewSet, basename='categories')
router.register(r'genres', CommentViewSet, basename='genres')
router.register(r'titles', CommentViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewAPI.as_view(), name='token_obtain_pair'),
    path(
        'v1/auth/signup/',
        EmailConfirmationViewSet.as_view(), name='regist_user_conf_email'),
]
