# Generated by Django 2.2.3 on 2021-11-30 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0032_auto_20211130_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
