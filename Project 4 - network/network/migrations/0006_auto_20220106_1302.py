# Generated by Django 2.2.3 on 2022-01-06 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_post_following_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post_following',
            name='post',
        ),
        migrations.AddField(
            model_name='post_following',
            name='content',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='post_following',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='post_following',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
