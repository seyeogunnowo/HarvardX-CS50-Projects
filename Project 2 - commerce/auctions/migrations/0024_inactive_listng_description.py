# Generated by Django 2.2.3 on 2021-11-29 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0023_auto_20211129_0846'),
    ]

    operations = [
        migrations.AddField(
            model_name='inactive_listng',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
