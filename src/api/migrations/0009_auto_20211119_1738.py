# Generated by Django 2.2 on 2021-11-19 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20211115_1548'),
    ]

    operations = [
        migrations.AlterField(
            model_name='household',
            name='surveyversionnumber',
            field=models.ForeignKey(default=995, on_delete=django.db.models.deletion.PROTECT, to='api.HouseholdSurveyVersion'),
        ),
    ]
