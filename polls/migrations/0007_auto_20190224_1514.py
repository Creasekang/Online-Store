# Generated by Django 2.1.4 on 2019-02-24 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_order_food_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_info',
            name='address',
            field=models.CharField(default='无', max_length=100),
        ),
        migrations.AddField(
            model_name='user_info',
            name='photo_num',
            field=models.CharField(default='无', max_length=100),
        ),
    ]
