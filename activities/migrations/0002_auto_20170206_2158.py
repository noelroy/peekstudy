# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-02-06 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='activity_type',
            field=models.CharField(choices=[('L', 'Like')], max_length=1),
        ),
    ]
