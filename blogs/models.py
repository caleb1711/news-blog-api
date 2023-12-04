from django.db import models
from django.conf import settings
from accounts.models import User
# Create your models here.

# Category
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category" 
        verbose_name_plural = "Categories"

    def __str__(self) :
        return f"{self.name}" or f"Blog-{self.id}"

# Blog Model
class Blog(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="c_blogs", help_text=("Add the Category"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs", help_text=("Add the owner of blog"))
    image = models.ImageField(upload_to="blog_images/", help_text=("Add Blog image"))
    title = models.CharField(max_length=500, help_text=("Add Blog title"))
    content = models.TextField(help_text=("Add Blog content"))
    
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog" 
        verbose_name_plural = "Blogs"

    def __str__(self) :
        return f"{self.title}" or f"Blog-{self.id}"
    
# Comment Model
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentblogs", help_text=("Add the blog"))
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="comments", help_text=("Add the comment"))
    content = models.TextField(help_text=("Add Blog content"))
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Comment" 
        verbose_name_plural = "Comments"

    def __str__(self) :
        return f"{self.content}" or f"Comment-{self.id}"