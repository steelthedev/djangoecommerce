# Generated by Django 3.1.4 on 2020-12-27 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('istore', '0004_auto_20201227_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
