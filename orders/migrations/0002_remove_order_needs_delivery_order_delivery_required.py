# Generated by Django 4.2.8 on 2024-03-28 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='needs_delivery',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_required',
            field=models.BooleanField(default=False, verbose_name='Delivery required'),
        ),
    ]
