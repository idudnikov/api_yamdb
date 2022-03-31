from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from datetime import datetime
from reviews.models import Category, Genre, Title, Review, Comment

from users.models import CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category')

    def validate(self, data):
        if self.context['year'] > datetime.now().year:
            raise serializers.ValidationError(
                'Ошибка. Год создания произведения еще не наступил'
            )
        return data


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
