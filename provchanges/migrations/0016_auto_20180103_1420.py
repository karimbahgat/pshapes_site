# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-03 13:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provchanges', '0015_auto_20171230_0352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='source',
            name='is_resource',
        ),
        migrations.AddField(
            model_name='map',
            name='country',
            field=models.CharField(blank=True, max_length=40, verbose_name='Country'),
        ),
        migrations.AddField(
            model_name='source',
            name='country',
            field=models.CharField(blank=True, max_length=40, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='mapsources',
            field=models.ManyToManyField(blank=True, related_name='mapsources_set', to='provchanges.Map', verbose_name='Maps used for information'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='sources',
            field=models.ManyToManyField(blank=True, to='provchanges.Source', verbose_name='Sources of information'),
        ),
    ]
