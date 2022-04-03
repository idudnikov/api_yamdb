import re
from datetime import datetime

from django.db.models import Avg
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
