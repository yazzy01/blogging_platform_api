from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.db.models import Count
import logging

logger = logging.getLogger('apps')

class Category(models.Model):
    """
    Model representing a blog post category.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='children'
    )
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=7, default='#000000')
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="Optional SEO title")
    meta_description = models.CharField(max_length=160, blank=True, help_text="Optional SEO description")
    
    # Image field
    image = models.ImageField(upload_to='categories/%Y/%m/', blank=True, null=True)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'categories'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['parent']),
            models.Index(fields=['is_active']),
            models.Index(fields=['order']),
        ]
        
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        # Log category creation/update
        is_new = not self.pk
        if is_new:
            logger.info(f"Creating new category: {self.name}")
        else:
            logger.info(f"Updating category: {self.name}")

        # Clear cache
        cache.delete(f'category_{self.slug}')
        cache.delete('all_active_categories')
        super().save(*args, **kwargs)
        
    def delete(self, *args, **kwargs):
        # Clear cache
        cache.delete(f'category_{self.slug}')
        cache.delete('all_active_categories')
        super().delete(*args, **kwargs)
        
    def clean(self):
        """Validate the category data."""
        if self.parent and self.parent == self:
            raise ValidationError("A category cannot be its own parent.")
        
        if self.parent and self.parent.parent:
            raise ValidationError("Categories can only be nested one level deep.")

    @property
    def posts_count(self):
        """Get the number of posts in this category."""
        return self.posts.count()

    @property
    def all_children(self):
        """Get all child categories."""
        return self.children.filter(is_active=True)

    @property
    def has_children(self):
        """Check if category has any child categories."""
        return self.children.filter(is_active=True).exists()

    @property
    def breadcrumbs(self):
        """Get category breadcrumbs"""
        crumbs = []
        current = self
        while current is not None:
            crumbs.append(current)
            current = current.parent
        return list(reversed(crumbs))
        
    @property
    def full_name(self):
        """Get full category name including parents"""
        return ' > '.join(cat.name for cat in self.breadcrumbs)
        
    def get_descendants(self, include_self=False):
        """Get all descendant categories"""
        descendants = []
        if include_self:
            descendants.append(self)
        for child in self.children.all():
            descendants.extend(child.get_descendants(include_self=True))
        return descendants
        
    @classmethod
    def get_active_categories(cls):
        """Get all active categories with their post counts."""
        return cls.objects.filter(is_active=True).annotate(
            total_posts=Count('posts')
        ).order_by('-total_posts')

    @classmethod
    def get_category_tree(cls):
        """Get a hierarchical tree of categories."""
        return cls.objects.filter(
            parent=None,
            is_active=True
        ).prefetch_related('children')
