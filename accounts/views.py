from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import SlidingToken
from accounts.serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserChangePasswordSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)

User = get_user_model()


class UserViewset(GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin):
    def get_serializer_class(self):
        if self.action == "create":
            return UserSerializer
        if self.action == "change_password":
            return UserChangePasswordSerializer
        if self.action == "forget_password":
            return ForgotPasswordSerializer
        return UserProfileSerializer

    def get_queryset(self):
        return User.objects.filter(user=self.request.user)

    def get_object(self):
        return self.request.user

    def list(self, *args, **kwargs):
        return self.retrieve(*args, **kwargs)

    @action(detail=False, methods=["post"], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)

    @action(detail=False, methods=["post"])
    def forget_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "An email is sent to your email address."})


class ResetPassword(APIView):
    def post(self, request, uid, token, format=None):
        serializer = ResetPasswordSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"msg": "Password Changed Successfully"}, status=status.HTTP_200_OK
        )
