# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-02 09:28
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provchanges', '0024_auto_20180602_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provchange',
            name='fromcapitalmove',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='From province capital (moved)'),
        ),
        migrations.AlterField(
            model_name='provchange',
            name='tocapitalmove',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='To province capital (moved)'),
        ),
    ]