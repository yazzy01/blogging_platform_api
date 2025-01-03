from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache
from django.db import connection, reset_queries
from apps.posts.models import Post
from apps.categories.models import Category
from django.utils.text import slugify
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from datetime import datetime

User = get_user_model()

@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    },
    DEBUG=True
)
class PostPerformanceTests(TestCase):
    def setUp(self):
        cache.clear()  # Clear cache before each test
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='Technology',
            description='Tech posts'
        )
        
        # Create multiple posts for testing
        self.posts = []
        for i in range(10):
            post = Post.objects.create(
                title=f'Test Post {i}',
                content=f'Content for test post {i} that is longer than 20 characters for validation.',
                author=self.user,
                category=self.category,
                status='published',  # Make posts published by default
                slug=slugify(f'Test Post {i}')
            )
            self.posts.append(post)

    def test_query_optimization(self):
        """Test the number of queries executed for listing posts"""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse('post-list'))
            
        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        print(f"Number of queries executed: {query_count}")
        self.assertLess(query_count, 10)

    def test_query_optimization_with_filters(self):
        """Test query performance with filters applied"""
        # Format dates in YYYY-MM-DD format
        start_date = '2024-01-01'
        end_date = '2024-12-31'
        
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(
                f'{reverse("post-list")}?category={self.category.id}'
                f'&start_date={start_date}'
                f'&end_date={end_date}'
            )
            
        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        print(f"Number of queries with filters: {query_count}")
        self.assertLess(query_count, 10)

    def test_query_optimization_with_search(self):
        """Test query performance with search"""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(f'{reverse("post-list")}?search=test')
            
        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        print(f"Number of queries with search: {query_count}")
        self.assertLess(query_count, 10)

    def test_single_post_query_performance(self):
        """Test the number of queries for retrieving a single post"""
        post = self.posts[0]
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(reverse('post-detail', kwargs={'slug': post.slug}))
            
        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        print(f"Number of queries for single post: {query_count}")
        self.assertLess(query_count, 6)  # Allow for a few more queries due to related fields

    def test_create_post_performance(self):
        """Test the number of queries for creating a post"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Performance Test Post',
            'content': 'Content for performance test post that is longer than 20 characters.',
            'excerpt': 'Test excerpt',
            'category': self.category.id,
            'status': 'published'
        }
        with CaptureQueriesContext(connection) as context:
            response = self.client.post(reverse('post-list'), data, format='json')
            
        self.assertEqual(response.status_code, 201)
        query_count = len(context.captured_queries)
        print(f"Number of queries for creating post: {query_count}")
        self.assertLess(query_count, 10)

    def tearDown(self):
        """Clean up after tests"""
        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
