# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BigIntegerField(default=False, verbose_name='\u5df2\u5220\u9664')),
                ('name', models.CharField(max_length=250, verbose_name='\u540d\u5b57')),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u535a\u5ba2',
                'verbose_name_plural': '\u535a\u5ba2\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BigIntegerField(default=False, verbose_name='\u5df2\u5220\u9664')),
                ('title', models.CharField(max_length=250, verbose_name='\u6807\u9898')),
                ('content', models.TextField(null=True, verbose_name='\u5185\u5bb9', blank=True)),
                ('blog', models.ForeignKey(verbose_name='\u6240\u5c5e\u535a\u5ba2', to='demo.Blog')),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0\u7ba1\u7406',
            },
            bases=(models.Model,),
        ),
    ]
