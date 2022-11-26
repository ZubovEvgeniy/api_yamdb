from rest_framework import serializers, exceptions

from reviews.models import User, Category, Genre, Title, Review, Comment
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        model = User


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email')
        model = User

        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email'],
            )
        ]

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                {
                    'username': ('Такое имя уже занято!')
                }
            )
        return value


class UserGetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ('id',)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ('id',)


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'category',
            'genre',
            'year',
            'rating'
        )
        read_only_fields = ('__all__',)


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        queryset=Genre.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'description',
            'category',
            'genre',
            'year'
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(
                title=self.context['view'].kwargs.get('title_id'),
                author=self.context['request'].user
            ).exists():
                raise exceptions.ValidationError(
                    'Данный пользователь уже добавил '
                    'отзыв для этого произведения. '
                    'Один пользователь может добавить '
                    'только один отзыв.'
                )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )

    class Meta:
        model = Comment
        fields = '__all__'
