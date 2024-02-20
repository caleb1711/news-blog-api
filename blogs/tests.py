from PIL import Image
from io import BytesIO
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from .models import Blog, Category




# Test Cases for User Blog API
class UserBlogApiTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='Test Category')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='This is a test blog',
            user=self.user,
            category=self.category
        )

    def test_list_user_blogs(self):
        url = '/api/blog/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) 

    def _generate_test_image(self):
        image = Image.new('RGB', (100, 100), 'white')
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        image_io.name = 'test_image.jpg'  
        return image_io



    def test_create_user_blog(self):
        category = Category.objects.create(name='crime')
        image = self._generate_test_image()
    
        url = '/api/blog/'
        data = {
            'title': 'New Blog',
            'content': 'This is a new blog',
            'category': category.id,
            'image': image
        }
        response = self.client.post(url, data, format='multipart')
        if response.status_code != status.HTTP_201_CREATED:
            print(response.data)  
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Blog.objects.count(), 2)


    def test_retrieve_user_blog(self):
        url = f'/api/blog/{self.blog.pk}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Blog')

    def test_update_user_blog(self):
        url = f'/api/blog/{self.blog.pk}/'
        category = Category.objects.create(name='crime')
        image = self._generate_test_image()


        data = {
            'title': 'Updated Blog',
            'content': 'This is an updated blog',
            'category': category.id,
            'image': image
        }
        response = self.client.put(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.title, 'Updated Blog')
    def test_delete_user_blog(self):
        url = f'/api/blog/{self.blog.pk}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Blog.objects.filter(pk=self.blog.pk).exists())


# Test Cases for Public Blog API

class PublicBlogAPITestCase(APITestCase):
    def test_list_public_blogs(self):
        url = '/api/blog/public/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_title(self):
        blog = Blog.objects.first() 
        if blog:
            title = blog.title
        url = f'/api/blog/public/?search={title}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_content(self):
        blog = Blog.objects.first() 
        if blog:
            content = blog.content
        url = f'/api/blog/public/?search={content}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_category_name(self):
        blog = Blog.objects.first() 
        if blog:
            category_name = blog.category.name
        url = f'/api/blog/public/?search={category_name}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# Test Cases for Like Action Endpoint

class LikeActionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='NewCategory')
        self.blog = Blog.objects.create(
            title='Test Blog for Like',
            content='This is a test blog for like',
            user=self.user,
            category=self.category
        )
    def test_like_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = f'/api/blog/public/{self.blog.pk}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = f'/api/blog/public/{self.blog.pk}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.user in self.blog.likes.all()) 

    def test_unlike_authenticated(self):
        self.blog.likes.add(self.user)
        self.client.force_authenticate(user=self.user)
        url = f'/api/blog/public/{self.blog.pk}/like/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(self.user not in self.blog.likes.all()) 


# Test Cases for Comment Action Endpoint

class CommentActionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@example.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.category = Category.objects.create(name='NewCategory')
        self.blog = Blog.objects.create(
            title='Test Blog for Comment',
            content='This is a test blog for comment',
            user=self.user,
            category=self.category
        )
    def test_comment_unauthenticated(self):
        self.client.force_authenticate(user=None)
        url = f'/api/blog/public/{self.blog.pk}/comment/'
        data = {'text': 'Test comment'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_comment_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = f'/api/blog/public/{self.blog.pk}/comment/'
        data = {'content': 'Test comment', 'blog': self.blog.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['content'], 'Test comment')
        self.assertEqual(response.data['user']['email'], self.user.email) 
        self.assertEqual(response.data['blog'], self.blog.pk)
