# Generated by Django 3.1.4 on 2021-01-02 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('istore', '0017_auto_20210102_0948'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]