# Generated by Django 2.2 on 2021-10-14 00:46

import api.models.base
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20211014_0046'),
    ]

    operations = [
        migrations.AddField(
            model_name='birth',
            name='dateofdeath',
            field=models.PositiveSmallIntegerField(default=995, validators=[api.models.base.MinValueBCValidator(2000), api.models.base.MaxValueBCValidator(2021)]),
        ),
        migrations.AddField(
            model_name='death',
            name='datedeath',
            field=models.PositiveSmallIntegerField(default=995, validators=[api.models.base.MinValueBCValidator(2000), api.models.base.MaxValueBCValidator(2021)]),
        ),
    ]
