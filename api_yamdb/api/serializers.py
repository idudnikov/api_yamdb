import re
from datetime import datetime

from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers


from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate_slug(self, value):
        reg = re.compile('^[-a-zA-Z0-9_]+$')
        if not reg.match(value):
            raise serializers.ValidationError(
                'Такую комбинацию нельзя использовать в качестве slug')
        return value


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate_slug(self, value):
        reg = re.compile('^[-a-zA-Z0-9_]+$')
        if not reg.match(value):
            raise serializers.ValidationError(
                'Такую комбинацию нельзя использовать в качестве slug')
        return value


class TitleSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(TitleSerializer, self).__init__(*args, **kwargs)
        if self.context['request'].method in ['POST', 'PATCH']:
            self.fields['category'] = serializers.SlugRelatedField(
                slug_field='slug',
                read_only=False,
                queryset=Category.objects.all()
            )
            self.fields['genre'] = serializers.SlugRelatedField(
                many=True,
                slug_field='slug',
                read_only=False,
                queryset=Genre.objects.all(),
            )

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField(read_only=True, )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def validate_year(self, value):
        if value > datetime.now().year:
            raise serializers.ValidationError(
                'Ошибка. Год создания произведения еще не наступил'
            )
        return value

    def get_rating(self, title):
        rating = Review.objects.filter(title=title).aggregate(Avg('score'))
        if rating.get('score__avg') is None:
            return None
        return int(rating.get('score__avg'))


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        super().validate(data)
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                "Вы уже оставили отзыв на данное произведение")
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class CreateCustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                {"Wrong username": "User 'me' can not be created."}
            )
        return data


class TokenSerializer(serializers.ModelSerializer):
    """Class TokenSerializer."""

    username = serializers.CharField(write_only=True)
    confirmation_code = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']

    def validate_username(self, value):
        get_object_or_404(CustomUser, username=value)
        return value

    def validate(self, data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(CustomUser, username=username)
        if not user:
            raise serializers.ValidationError({
                "Wrong username or confirmation code":
                    "Please input correct data."
            })
        if not default_token_generator.check_token(user, confirmation_code):
            raise serializers.ValidationError({
                'confirmation_code': ['Invalid value']})
        return data
