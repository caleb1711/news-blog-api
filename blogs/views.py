from rest_framework import viewsets 
from rest_framework import permissions 
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from .models import Blog, Category
from .serializers  import BlogSerializer, UserBlogsApi, CategorySerializer, CommentSerializer


class UserBlogApi(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = UserBlogsApi

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        return Blog.objects.filter(user=self.request.user).select_related("category")


class BlogPublicViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Blog.objects.all().select_related("category").annotate(total_likes=Count("likes"))
    
    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogSerializer
        return BlogSerializer

    filter_backends = [OrderingFilter, SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'content', 'category__name']
    ordering_fields = ['category', 'title']
    filterset_fields = ["category", "title", "category__name"]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'post']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
        

    @action(detail=True, methods=['put'])
    def like(self, request, pk=None):
        blog = self.get_object()
    
        if request.user.is_authenticated:
            user = request.user

            if user in blog.likes.all():
                blog.likes.remove(user)
            else:
                blog.likes.add(user)

            return Response({"message": "Like Added"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message": "Authentication required to like the blog"}, status=status.HTTP_401_UNAUTHORIZED)


    @action(detail=True, methods=['post'])
    def comment(self, request, pk=None):
        blog = self.get_object()
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(blog=blog, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        



class CategoryViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
