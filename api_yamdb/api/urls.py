from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .emailconfirmation import EmailConfirmationViewSet
from . import views
from .tokens import TokenViewAPI

app_name = 'api'

router = DefaultRouter()

router.register(r'users', views.CommentViewSet, basename='users')
router.register(r'categories', views.CategoryViewSet, basename='categories')
router.register(r'genres', views.GenreViewSet, basename='genres')
router.register(r'titles', views.TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews',
    views.ReviewViewSet,
    basename='reviews')
router.register(
    r'titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
    views.CommentViewSet,
    basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenViewAPI.as_view(), name='token_obtain_pair'),
    path(
        'v1/auth/signup/',
        EmailConfirmationViewSet.as_view(), name='regist_user_conf_email'),
]
