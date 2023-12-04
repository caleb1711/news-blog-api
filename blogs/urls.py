from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserBlogApi, BlogPublicViewSet, CategoryViewset

app_name = "blog"
router = DefaultRouter()
router.register("public", BlogPublicViewSet, basename="public-blog")
router.register("categories", CategoryViewset, basename="categories")
router.register("", UserBlogApi, basename="blogapi")


urlpatterns = router.urls
