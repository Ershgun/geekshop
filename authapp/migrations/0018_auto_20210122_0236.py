# Generated by Django 2.2.17 on 2021-01-21 21:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0017_auto_20210120_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 23, 21, 36, 12, 145438, tzinfo=utc)),
        ),
    ]
