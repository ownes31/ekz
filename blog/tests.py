from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Post, Comment

class BlogAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_post(self):
        response = self.client.post('/api/posts/', {'title': 'Test Post', 'content': 'Test Content'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['title'], 'Test Post')

    def test_get_posts(self):
        Post.objects.create(title='A', content='B', author=self.user)
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_post_detail(self):
        post = Post.objects.create(title='A', content='B', author=self.user)
        response = self.client.get(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'A')

    def test_update_post(self):
        post = Post.objects.create(title='A', content='B', author=self.user)
        response = self.client.patch(f'/api/posts/{post.id}/', {'title': 'New Title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'New Title')

    def test_delete_post(self):
        post = Post.objects.create(title='A', content='B', author=self.user)
        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, 204)

    def test_add_comment(self):
        post = Post.objects.create(title='A', content='B', author=self.user)
        response = self.client.post(f'/api/posts/{post.id}/comments/', {'text': 'Nice!'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['text'], 'Nice!')

    def test_get_comments(self):
        post = Post.objects.create(title='A', content='B', author=self.user)
        Comment.objects.create(post=post, text='Nice!', author=self.user)
        response = self.client.get(f'/api/posts/{post.id}/comments/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) >= 1)

    def test_search_post(self):
        Post.objects.create(title='UniqueTitle', content='B', author=self.user)
        response = self.client.get('/api/posts/?search=UniqueTitle')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(any('UniqueTitle' in post['title'] for post in response.data))
