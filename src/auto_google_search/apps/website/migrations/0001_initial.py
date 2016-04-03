# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchExtractedInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('extracted_info_key', models.CharField(max_length=100)),
                ('extracted_info_value', models.TextField(default=None, max_length=50000, null=True, blank=True)),
            ],
            options={
                'db_table': 'ags_search_extracted_info',
            },
        ),
        migrations.CreateModel(
            name='SearchRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('search_term', models.CharField(max_length=500)),
                ('search_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('is_successful', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-search_timestamp'],
                'db_table': 'ags_search_record',
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=500)),
                ('order', models.SmallIntegerField(default=0)),
                ('search_record', models.ForeignKey(related_name='results', to='website.SearchRecord')),
            ],
            options={
                'ordering': ['order'],
                'db_table': 'ags_search_result',
            },
        ),
        migrations.AddField(
            model_name='searchextractedinfo',
            name='search_result',
            field=models.ForeignKey(related_name='extracted_info', to='website.SearchResult'),
        ),
    ]
