# Generated by Django 2.2.3 on 2021-11-29 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_comment_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inactive_Listng',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, null=True)),
                ('title', models.CharField(max_length=30)),
                ('starting_bid', models.IntegerField()),
                ('winning_bid', models.IntegerField()),
            ],
        ),
    ]