# Generated by Django 2.1.4 on 2019-02-23 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20190223_1922'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='food',
        ),
        migrations.RemoveField(
            model_name='order',
            name='food_price',
        ),
        migrations.AddField(
            model_name='order',
            name='can_buy',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='cost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='food_id',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='food_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='order',
            name='has_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='has_pay',
            field=models.BooleanField(default=False),
        ),
    ]