# Generated by Django 4.2.17 on 2024-12-20 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RenameIndex(
            model_name='post',
            new_name='posts_post_created_183a3b_idx',
            old_name='posts_post_created_2a1cba_idx',
        ),
        migrations.RenameIndex(
            model_name='post',
            new_name='posts_post_slug_59b922_idx',
            old_name='posts_post_slug_0c7d0c_idx',
        ),
        migrations.RenameIndex(
            model_name='post',
            new_name='posts_post_status_79fb4e_idx',
            old_name='posts_post_status_bd6c3a_idx',
        ),
    ]
