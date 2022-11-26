from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from api.v1.serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserGetTokenSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleGetSerializer,
    TitlePostSerializer,
    ReviewSerializer,
    CommentSerializer
)
from api.v1.permissions import (
    AdminPermission,
    IsAuthorAdminModerOrReadOnly,
    IsAdminOrReadOnly,
)
from api.v1.mixins import MixinSet
from api.v1.filters import TitleFilter
from reviews.models import User, Category, Genre, Title, Review
from api_yamdb.settings import EMAIL_ROBOT


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminPermission,)
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        serializer = self.get_serializer(request.user)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.validated_data['role'] = request.user.role
                serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения регистрации',
                f'{confirmation_code}',
                EMAIL_ROBOT,
                [serializer.validated_data.get('email')],
            )
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserGetTokenView(APIView):
    def post(self, request):
        serializer = UserGetTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data.get('username')
            user = get_object_or_404(User, username=username)
            token = serializer.validated_data.get('confirmation_code')
            confirmation_code = default_token_generator.check_token(
                user, token)
            if not confirmation_code:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            refresh = RefreshToken.for_user(user)
            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['=name']
    lookup_field = 'slug'


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['=name']
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorAdminModerOrReadOnly,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorAdminModerOrReadOnly,)

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)
