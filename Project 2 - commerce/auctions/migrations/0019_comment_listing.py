# Generated by Django 2.2.3 on 2021-11-27 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20211127_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='listing',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
