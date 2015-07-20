# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tmkit.db.field


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RuntimeConfItem',
            fields=[
                ('key', models.CharField(primary_key=True, serialize=False, max_length=250, help_text='\u6700\u957f250', unique=True, verbose_name='\u952e')),
                ('value', tmkit.db.field.PythonObjectField(help_text='\u6700\u957f250', max_length=250, null=True, verbose_name='\u914d\u7f6e\u503c', blank=True)),
                ('info', models.TextField(null=True, verbose_name='\u914d\u7f6e\u8bf4\u660e', blank=True)),
            ],
            options={
                'verbose_name': '\u8fd0\u884c\u65f6\u914d\u7f6e',
                'verbose_name_plural': '\u8fd0\u884c\u65f6\u914d\u7f6e\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RuntimeConfItemProxy',
            fields=[
            ],
            options={
                'verbose_name': '\u8fd0\u884c\u65f6\u914d\u7f6e',
                'proxy': True,
                'verbose_name_plural': '\u8fd0\u884c\u65f6\u914d\u7f6e\u7ba1\u7406',
            },
            bases=('runtime_conf.runtimeconfitem',),
        ),
    ]
