# Generated by Django 4.2.17 on 2024-12-20 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='is_approved',
            new_name='is_active',
        ),
        migrations.AddField(
            model_name='comment',
            name='moderated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='moderated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='moderated_comments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['created_at'], name='comments_co_created_5f6a12_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['status'], name='comments_co_status_2720ea_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['is_active'], name='comments_co_is_acti_69743a_idx'),
        ),
    ]