# Generated by Django 4.1.7 on 2023-10-09 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0008_remove_order_order_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
