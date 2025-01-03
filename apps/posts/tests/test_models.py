from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.cache import cache
from apps.posts.models import Post, Tag
from apps.categories.models import Category

User = get_user_model()

@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
)
class PostModelTest(TestCase):
    def setUp(self):
        cache.clear()  # Clear cache before each test
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
            status='published'
        )
        self.post.tags.add(self.tag)

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.slug, slugify('Test Post'))
        self.assertEqual(self.post.author, self.user)
        self.assertEqual(self.post.category, self.category)
        self.assertEqual(self.post.tags.count(), 1)
        self.assertEqual(self.post.tags.first(), self.tag)

    def test_post_str_representation(self):
        self.assertEqual(str(self.post), 'Test Post')

    def test_auto_slug_generation(self):
        post = Post.objects.create(
            title='Another Test Post',
            content='Another Test Content',
            author=self.user,
            category=self.category
        )
        self.assertEqual(post.slug, slugify('Another Test Post'))

    def test_increment_views(self):
        initial_views = self.post.views
        self.post.increment_views()
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, initial_views + 1)

@override_settings(
    CACHES={
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake',
        }
    }
)
class TagModelTest(TestCase):
    def setUp(self):
        cache.clear()  # Clear cache before each test
        self.tag = Tag.objects.create(name='Test Tag')

    def test_tag_creation(self):
        self.assertEqual(self.tag.name, 'Test Tag')
        self.assertEqual(self.tag.slug, slugify('Test Tag'))

    def test_tag_str_representation(self):
        self.assertEqual(str(self.tag), 'Test Tag')

    def test_auto_slug_generation(self):
        tag = Tag.objects.create(name='Another Test Tag')
        self.assertEqual(tag.slug, slugify('Another Test Tag'))
