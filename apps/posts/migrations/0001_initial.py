from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('content', models.TextField()),
                ('excerpt', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published')], default='draft', max_length=10)),
                ('views', models.PositiveIntegerField(default=0)),
                ('meta_title', models.CharField(blank=True, max_length=200)),
                ('meta_description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='categories.category')),
                ('tags', models.ManyToManyField(blank=True, to='posts.tag')),
            ],
            options={
                'ordering': ['-created_at'],
                'indexes': [
                    models.Index(fields=['-created_at'], name='posts_post_created_2a1cba_idx'),
                    models.Index(fields=['slug'], name='posts_post_slug_0c7d0c_idx'),
                    models.Index(fields=['status'], name='posts_post_status_bd6c3a_idx'),
                ],
            },
        ),
    ]
