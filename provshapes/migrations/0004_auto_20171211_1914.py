# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-11 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provshapes', '0003_auto_20171211_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provshape',
            name='alterns',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='provshape',
            name='fips',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='provshape',
            name='hasc',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='provshape',
            name='iso',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
