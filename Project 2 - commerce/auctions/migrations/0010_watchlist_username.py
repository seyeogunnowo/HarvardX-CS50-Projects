# Generated by Django 2.2.3 on 2021-11-26 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_bid_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='username',
            field=models.CharField(max_length=30, null=True),
        ),
    ]