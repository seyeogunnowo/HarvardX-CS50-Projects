# Generated by Django 2.2.3 on 2022-01-26 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_post_following_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='post_following',
            name='date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]
