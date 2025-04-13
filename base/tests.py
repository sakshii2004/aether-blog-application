from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Blog, Comment
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

class BlogAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.blog = Blog.objects.create(
            title='Test Blog',
            content='This is a test blog.',
            author=self.user
        )

    def test_landing_page_status_code(self):
        response = self.client.get(reverse('landing-page'))
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'first_name': 'First',
            'last_name': 'Last',
            'email': 'newuser@example.com',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123'
        })
        self.assertEqual(response.status_code, 302)  # should redirect
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_user(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # should redirect

    def test_create_blog(self):
        self.client.login(username='testuser', password='password123')
        image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        response = self.client.post(reverse('create-blog'), {
            'title': 'Another Blog',
            'content': 'More content here.',
            'image': image
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Blog.objects.filter(title='Another Blog').exists())

    def test_comment_on_blog(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('read-blog', args=[self.blog.id]), {
            'body': 'Nice post!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(blog=self.blog, user=self.user).exists())

    def test_like_blog(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('like-blog', args=[self.blog.id]))
        self.blog.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.blog.number_of_likes, 1)
        self.assertIn(self.user, self.blog.liked_by.all())

    def test_unlike_blog(self):
        self.blog.liked_by.add(self.user)
        self.blog.number_of_likes = 1
        self.blog.save()
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('like-blog', args=[self.blog.id]))
        self.blog.refresh_from_db()
        self.assertEqual(self.blog.number_of_likes, 0)
        self.assertNotIn(self.user, self.blog.liked_by.all())

