# Generated by Django 2.2.3 on 2022-02-02 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0014_auto_20220202_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users_Following',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
