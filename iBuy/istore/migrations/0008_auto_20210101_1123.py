# Generated by Django 3.1.4 on 2021-01-01 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('istore', '0007_auto_20201229_2040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderitem',
            old_name='products',
            new_name='product',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='istore.categories'),
        ),
    ]