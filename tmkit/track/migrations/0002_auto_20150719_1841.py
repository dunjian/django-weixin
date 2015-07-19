# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('track', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name': '\u8bf7\u6c42\u65e5\u5fd7', 'verbose_name_plural': '\u8bf7\u6c42\u65e5\u5fd7\u7ba1\u7406'},
        ),
        migrations.AlterField(
            model_name='entry',
            name='content',
            field=models.TextField(verbose_name='\u54cd\u5e94\u6587\u4ef6\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='size',
            field=models.IntegerField(verbose_name='\u8bf7\u6c42\u5927\u5c0f(request.body)'),
        ),
    ]
