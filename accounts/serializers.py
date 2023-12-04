import threading
import uuid

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings
from rest_framework import serializers
from rest_framework_simplejwt.tokens import SlidingToken

from .emails import send_email
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")
        extra_kwargs ={
            'password' :{"write_only":True}
        }

    def validate(self, attrs):
        if User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError("User with this email is already exists.")
        if len(attrs.get("password")) < 8:
            raise serializers.ValidationError("Password length should be at least 8 characters.")
        return super().validate(attrs)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        subject = "Welcome to our Website!"
        text_content = "Welome"
        recipient_list = [user.email]
        html_template = "email.html"
        context = {"name": user.first_name}
        thread = threading.Thread(target=send_email, args = (subject, text_content, recipient_list, html_template, context,True ))
        thread.start()
        return user

    def to_representation(self, instance):
        user_data = super().to_representation(instance)
        return {
            "token": str(SlidingToken.for_user(instance)),
            "user": user_data
        }

    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ("email", "password")



class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email")
    

class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    password = serializers.CharField()
    password1 = serializers.CharField()

    class Meta:
        fields = ("old_password", "password", "password1")

    def validate_old_password(self, old_password):
        user = self.context['request'].user
        if not user.check_password(old_password):
            raise serializers.ValidationError("Old password is incorrect")
        return old_password

    def validate(self, attrs):
        password = attrs.get("passowrd")
        password1 = attrs.get("passowrd1")
        if password != password1:
            raise serializers.ValidationError("Both Password Should be same.")
        return attrs

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['password'])
        user.save()
        return user



class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("email",)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email is not exist in database.")
        return email
    
    def save(self, **validated_data):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token =  PasswordResetTokenGenerator().make_token(user)
        user.email_token = token
        user.save()
        url = f"{settings.FRONT_END_URL}/api/accounts/reset/{uid}/{token}/"
        subject = "Reset Password"
        text_content = "Hi"
        recipient_list = [email,]
        html_template = "reset-password.html"
        context = {"name": user.first_name, "link":url}
        thread = threading.Thread(target=send_email, args = (subject, text_content, recipient_list, html_template, context,True ))
        thread.start()
        return user
    

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    password1 = serializers.CharField()

    class Meta:
        fields = ("password", "password1")
    
    def validate(self, attrs):
        password = attrs.get("password")
        password1 = attrs.get("password1")
        if password != password1:
            raise serializers.ValidationError("Both Password Should be same.")
        
        uid = self.context.get("uid")
        token = self.context.get("token")
        id = smart_str(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
        print(user, "Id")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Token is Expired or Invalid")
        user.set_password(password)
        user.save()
        return user

