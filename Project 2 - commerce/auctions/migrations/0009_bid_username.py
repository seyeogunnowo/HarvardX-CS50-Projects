# Generated by Django 2.2.3 on 2021-11-26 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_auto_20211126_0654'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='username',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
