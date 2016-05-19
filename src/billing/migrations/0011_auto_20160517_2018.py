# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0010_auto_20160517_2017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 17, 20, 18, 24, 477018, tzinfo=utc), verbose_name=b'End Date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2016, 5, 17, 20, 18, 24, 477078, tzinfo=utc), verbose_name=b'Start Date'),
            preserve_default=True,
        ),
    ]
