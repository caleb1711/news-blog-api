from rest_framework import serializers
from blogs.models import Blog, Category, Comment
from accounts.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"

class BlogOwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "followers"]


class CommentSerializer(serializers.ModelSerializer):
    user = BlogOwnerSerializer(read_only=True, required=False)
    
    class Meta:
        model = Comment
        fields = "__all__"


class BlogSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    total_likes = serializers.IntegerField()
    user = BlogOwnerSerializer(read_only=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    liked = serializers.SerializerMethodField()
    class Meta:
        model = Blog
        fields = ['id' ,'category' , 'user',  'image', 'title', "comments", 'content', 'total_likes', 'created_at', 'updated_at', 'liked']

    def get_liked(self, instance):
        if hasattr(instance, "liked"):
            return instance.liked > 0
        return False

    def update(self, instance, validated_data):
        image_url = validated_data.get('image')
        if image_url:
            instance.image = image_url
        return super().update(instance, validated_data)


class UserBlogsApi(serializers.ModelSerializer):
    user = BlogOwnerSerializer(read_only=True)
    class Meta:
        model = Blog
        fields = ['id' ,'category' , 'user',  'image', 'title', 'content', 'created_at', 'updated_at']
        
    def update(self, instance, validated_data):
        image_url = validated_data.get('image')
        if image_url:
            validated_data.pop('image')
        return super().update(instance, validated_data)
