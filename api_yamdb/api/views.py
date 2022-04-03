from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status, mixins

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser

from .permissions import IsAdmin, IsOwnerOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer)


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdmin,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return (ReadOnly(),)
        return super().get_permissions()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = Review.objects.filter(title=title)
        return new_queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = Comment.objects.filter(review=review)
        return new_queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return Response(status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(BaseViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    search_fields = ('name',)

    def retrieve(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request)


class TitleViewSet(BaseViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')


class UsersViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_permissions(self):
        if self.kwargs.get('username') == 'me':
            return (IsAuthenticated(),)
        return super().get_permissions()

    def get_queryset(self):
        if self.kwargs.get('username') == 'me':
            return CustomUser.objects.get(username=self.request.user)
        return super().get_queryset()


class UserMeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = CustomUser.objects.get(username=request.user)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = CustomUser.objects.get(username=self.request.user)
        serializer = UserSerializer(data=request.data, instance=user,
                                    partial=True)
        role = self.request.user.role
        if serializer.is_valid():
            changed_role = serializer.validated_data.get('role')
            if role == 'admin':
                serializer.save()
            if role != 'admin' and changed_role is not None:
                serializer.validated_data['role'] = role
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
