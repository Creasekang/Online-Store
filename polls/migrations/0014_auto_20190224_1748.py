# Generated by Django 2.1.4 on 2019-02-24 09:48

from django.db import migrations, models
import polls.models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0013_auto_20190224_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food_info',
            name='food_img',
            field=models.ImageField(default='', upload_to=polls.models.user_path),
        ),
    ]
