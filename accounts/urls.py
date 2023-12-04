from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ResetPassword, UserViewset
from rest_framework_simplejwt.views import TokenObtainSlidingView, TokenRefreshSlidingView

app_name = "accounts"

router = DefaultRouter()
router.register('user', UserViewset, basename='signup')


urlpatterns = [
    path("login/", TokenObtainSlidingView.as_view(), name="login"),
    path("refresh/", TokenRefreshSlidingView.as_view(), name="refresh"),
    path("reset/<uid>/<token>/", ResetPassword.as_view(), name="reset"),
] + router.urls
