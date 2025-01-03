from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache
from apps.posts.models import Post, Tag
from apps.categories.models import Category
import json

User = get_user_model()

@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
)
class PostViewSetTest(TestCase):
    def setUp(self):
        cache.clear()  # Clear cache before each test
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Category Description'
        )
        self.tag = Tag.objects.create(name='Test Tag')
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            excerpt='Test Excerpt',
            author=self.user,
            category=self.category,
            status='draft'  # Changed to draft since we create published posts in test_list_posts
        )
        self.post.tags.add(self.tag)

    def tearDown(self):
        """Clean up after tests"""
        cache.clear()
        Post.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()
        Tag.objects.all().delete()

    def test_list_posts(self):
        cache.clear()  # Clear cache before test
        # Delete any existing posts
        Post.objects.all().delete()
        
        # Create one published post
        published_post = Post.objects.create(
            title='Published Post',
            content='Published Content',
            excerpt='Published Excerpt',
            author=self.user,
            category=self.category,
            status='published'
        )

        # Create some draft posts that shouldn't be visible
        Post.objects.create(
            title='Draft Post 1',
            content='Draft Content 1',
            excerpt='Draft Excerpt 1',
            author=self.user,
            category=self.category,
            status='draft'
        )
        Post.objects.create(
            title='Draft Post 2',
            content='Draft Content 2',
            excerpt='Draft Excerpt 2',
            author=self.user,
            category=self.category,
            status='draft'
        )

        # Test unauthenticated access - should only see published posts
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # 1 published post
        self.assertEqual(len(response.data['results']), 1)  # 1 published post

        # When authenticated as the author, should see all posts
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)  # 1 published + 2 draft posts
        self.assertEqual(len(response.data['results']), 3)  # 1 published + 2 draft posts

    def test_retrieve_post(self):
        response = self.client.get(
            reverse('post-detail', kwargs={'slug': self.post.slug})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_owner(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated Test Content',
            'excerpt': 'Updated Test Excerpt',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.put(
            reverse('post-detail', kwargs={'slug': self.post.slug}),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Test Post')

    def test_update_post_non_owner(self):
        # Create a published post for this test
        published_post = Post.objects.create(
            title='Published Post',
            content='Published Content',
            excerpt='Published Excerpt',
            author=self.user,
            category=self.category,
            status='published'
        )

        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        self.client.force_authenticate(user=other_user)
        data = {
            'title': 'Updated Test Post',
            'content': 'Updated Test Content',
            'excerpt': 'Updated Test Excerpt',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.put(
            reverse('post-detail', kwargs={'slug': published_post.slug}),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_posts(self):
        response = self.client.get(
            reverse('post-search'),
            {'q': 'Test'}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_posts_by_category(self):
        response = self.client.get(
            reverse('post-by-category'),
            {'slug': self.category.slug}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_filter_posts_by_tag(self):
        response = self.client.get(
            reverse('post-by-tag'),
            {'slug': self.tag.slug}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_draft_posts_authenticated(self):
        self.client.force_authenticate(user=self.user)
        Post.objects.create(
            title='Another Draft Post',
            content='Another Draft Content',
            excerpt='Another Draft Excerpt',
            author=self.user,
            category=self.category,
            status='draft'
        )
        response = self.client.get(reverse('post-drafts'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_draft_posts_unauthenticated(self):
        response = self.client.get(reverse('post-drafts'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Test Post',
            'content': 'New Test Content',
            'excerpt': 'New Test Excerpt',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.post(
            reverse('post-list'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_create_post_unauthenticated(self):
        data = {
            'title': 'New Test Post',
            'content': 'New Test Content',
            'excerpt': 'New Test Excerpt',
            'category': self.category.id,
            'status': 'published'
        }
        response = self.client.post(
            reverse('post-list'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
