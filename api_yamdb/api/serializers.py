import re
from datetime import datetime
from turtle import title

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title, GenreTitle
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
    genre = GenreSerializer(many=True, required=False)
    category = CategorySerializer()
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def validate(self, data):
        if self.context['year'] > datetime.now().year:
            raise serializers.ValidationError(
                'Ошибка. Год создания произведения еще не наступил'
            )
        return data

    def get_rating(self, obj):
        rating = Review.objects.filter(title=obj).aggregate(Avg('score'))
        return int(rating.get('score__avg'))

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title
        genres = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for genre in genres:
            current_genre = Genre.objects.get_or_create(
                **genre)
            GenreTitle.objects.get(
                genre=current_genre, title=title)
        return title

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Автор уже писал отзыв на данное произведение'
            )
        ]


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
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')
