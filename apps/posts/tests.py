from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Post
from apps.categories.models import Category
from django.utils.text import slugify

User = get_user_model()

class PostTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name='Technology',
            description='Tech posts'
        )

    def test_create_post(self):
        """Test creating a new blog post"""
        payload = {
            'title': 'Test Post Title',  # At least 5 characters
            'content': 'This is a test post content that is definitely longer than 20 characters.',  # At least 20 characters
            'status': 'published',
            'categories': [self.category.id],
            'excerpt': 'Test excerpt'
        }
        response = self.client.post('/api/posts/', payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(id=response.data['id'])
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.slug, slugify(payload['title']))

    def test_update_post(self):
        """Test updating a blog post"""
        # Create initial post
        post = Post.objects.create(
            title='Original Post Title',  # At least 5 characters
            content='This is the original content that is definitely longer than 20 characters.',  # At least 20 characters
            author=self.user,
            slug=slugify('Original Post Title')
        )
        
        # Add category to post
        post.categories.add(self.category)
        
        payload = {
            'title': 'Updated Post Title',
            'content': 'This is the updated content that is definitely longer than 20 characters.'
        }
        
        response = self.client.patch(f'/api/posts/{post.id}/', payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.title, payload['title'])
        self.assertEqual(post.content, payload['content'])

    def test_delete_post(self):
        """Test deleting a blog post"""
        post = Post.objects.create(
            title='Post to Delete',
            content='This is the content of the post that will be deleted. It needs to be long enough.',
            author=self.user,
            slug=slugify('Post to Delete')
        )
        
        response = self.client.delete(f'/api/posts/{post.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=post.id).exists())

    def test_unauthorized_update(self):
        """Test that users cannot update other users' posts"""
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='pass123'
        )
        
        post = Post.objects.create(
            title='Other User Post',
            content='This is a post by another user with content longer than 20 characters.',
            author=other_user,
            slug=slugify('Other User Post')
        )
        
        payload = {'title': 'Trying to update'}
        response = self.client.patch(f'/api/posts/{post.id}/', payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
