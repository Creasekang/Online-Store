# Generated by Django 2.1.4 on 2019-02-24 07:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0007_auto_20190224_1514'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_info',
            old_name='photo_num',
            new_name='phone_num',
        ),
    ]