from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.views import (
    UserRegistrationView,
    UserGetTokenView,
    UserViewSet,
    TitleViewSet,
    GenreViewSet,
    CategoryViewSet,
    ReviewViewset,
    CommentViewset
)


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genre')
router.register('titles', TitleViewSet, basename='title')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewset, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewset, basename='comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('auth/token/', UserGetTokenView.as_view(), name='token'),
]
