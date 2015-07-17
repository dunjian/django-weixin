# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u5df2\u5220\u9664'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='\u5df2\u5220\u9664'),
        ),
    ]
