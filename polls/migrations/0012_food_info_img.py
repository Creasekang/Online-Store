# Generated by Django 2.1.4 on 2019-02-24 09:26

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20190224_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='food_info',
            name='img',
            field=models.ImageField(default='', upload_to=polls.models.user_path),
        ),
    ]