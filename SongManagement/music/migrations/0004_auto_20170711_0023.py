# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-07-10 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_auto_20170710_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='file_type',
        ),
        migrations.AddField(
            model_name='album',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='album',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='album',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='song',
            name='audio_file',
            field=models.FileField(default='', upload_to=''),
        ),
        migrations.AlterField(
            model_name='album',
            name='album_logo',
            field=models.ImageField(height_field='height_field', upload_to='', width_field='width_field'),
        ),
    ]
