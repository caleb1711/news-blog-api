from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Blog, Category, Comment

User = get_user_model()

class BlogTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='test_password')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.blog = Blog.objects.create(title='Test Blog', content='Test Content', category=self.category, user=self.user)
        self.comment = Comment.objects.create(content='Test Comment', user=self.user, blog=self.blog)

    def test_create_blog(self):
        data = {
            'category': self.category.id,
            'title': 'New Test Blog',
            'content': 'New Test Content',
        }
        response = self.client.post('/blogs/blogapi/', data)
        self.assertEqual(response.status_code, 201)

    def test_list_blogs(self):
        response = self.client.get('/blogs/blogapi/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_blog(self):
        response = self.client.get(f'/blogs/blogapi/{self.blog.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Test Blog')

    def test_like_blog(self):
        response = self.client.post(f'/blogs/public/{self.blog.id}/like/')
        self.assertEqual(response.status_code, 204)

    def test_create_comment(self):
        data = {'content': 'New Test Comment'}
        response = self.client.post(f'/blogs/public/{self.blog.id}/comment/', data)
        self.assertEqual(response.status_code, 201)

    def test_list_comments(self):
        response = self.client.get(f'/blogs/public/{self.blog.id}/comment/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_categories(self):
        response = self.client.get('/blogs/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_category(self):
        response = self.client.get(f'/blogs/categories/{self.category.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Category')
