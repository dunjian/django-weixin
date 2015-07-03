# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.TextField(verbose_name='\u8bf7\u6c42\u8def\u5f84')),
                ('method', models.CharField(max_length=10, verbose_name='\u65b9\u6cd5')),
                ('body', models.TextField(verbose_name='\u8bf7\u6c42\u4f53')),
                ('size', models.IntegerField(verbose_name='\u8bf7\u6c42\u5927\u5c0f')),
                ('request_header', models.TextField(verbose_name='\u8bf7\u6c42\u5934')),
                ('request_time', models.DateTimeField(verbose_name='\u8bf7\u6c42\u65f6\u95f4')),
                ('response_header', models.TextField(verbose_name='\u54cd\u5e94\u5934')),
                ('status_code', models.IntegerField(verbose_name='\u8fd4\u56de\u72b6\u6001')),
                ('content', models.TextField(verbose_name='\u5e94\u7b54\u5185\u5bb9')),
                ('cost_time', models.IntegerField(verbose_name='\u54cd\u5e94\u65f6\u95f4(ms)')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
