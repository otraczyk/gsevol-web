# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-07 21:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('name', models.CharField(db_index=True, max_length=100)),
                ('gene', models.BooleanField(default=False)),
                ('species', models.BooleanField(default=False)),
                ('mapping', models.BooleanField(default=False)),
                ('embedding', models.BooleanField(default=False)),
                ('diagram', models.BooleanField(default=False)),
                ('html_input', models.CharField(max_length=100)),
                ('scope', models.CharField(blank=True, default='', max_length=100)),
                ('verbose_scope', models.CharField(blank=True, default='', max_length=100)),
                ('type', models.CharField(max_length=100)),
                ('default', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=100)),
            ],
        ),
    ]
