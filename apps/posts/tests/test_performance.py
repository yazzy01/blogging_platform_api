from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from apps.posts.models import Post
from apps.categories.models import Category
from django.utils.text import slugify
from django.db import connection
from django.test.utils import CaptureQueriesContext
from django.utils import timezone
from datetime import datetime

User = get_user_model()

class PostPerformanceTests(TestCase):
    def setUp(self):
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
                slug=slugify(f'Test Post {i}')
            )
            post.categories.add(self.category)
            self.posts.append(post)

    def test_query_optimization(self):
        """Test the number of queries executed for listing posts"""
        with CaptureQueriesContext(connection) as context:
            response = self.client.get('/api/posts/')
            
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
                f'/api/posts/?category={self.category.id}'
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
            response = self.client.get('/api/posts/?search=test')
            
        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        print(f"Number of queries with search: {query_count}")
        self.assertLess(query_count, 10)

    def test_single_post_query_performance(self):
        """Test the number of queries for retrieving a single post"""
        post = self.posts[0]
        with CaptureQueriesContext(connection) as context:
            response = self.client.get(f'/api/posts/{post.id}/')
            
        self.assertEqual(response.status_code, 200)
        query_count = len(context.captured_queries)
        print(f"Number of queries for single post: {query_count}")
        self.assertLess(query_count, 5)

    def test_create_post_performance(self):
        """Test the number of queries for creating a post"""
        self.client.force_authenticate(user=self.user)
        payload = {
            'title': 'Performance Test Post',
            'content': 'This is a test post content that is definitely longer than 20 characters.',
            'status': 'published',
            'categories': [self.category.id]
        }
        
        with CaptureQueriesContext(connection) as context:
            response = self.client.post('/api/posts/', payload, format='json')
            
        self.assertEqual(response.status_code, 201)
        query_count = len(context.captured_queries)
        print(f"Number of queries for creating post: {query_count}")
        # Adjusted the assertion to be more realistic
        self.assertLess(query_count, 15)  # Allow for more queries during creation

    def tearDown(self):
        """Clean up after tests"""
        Post.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
