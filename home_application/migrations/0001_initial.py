# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Scritpt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('desc', models.CharField(max_length=16)),
                ('content', models.TextField(max_length=2000)),
                ('type', models.CharField(max_length=16)),
                ('source', models.CharField(max_length=16)),
                ('version', models.IntegerField()),
                ('creator', models.CharField(max_length=20)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
