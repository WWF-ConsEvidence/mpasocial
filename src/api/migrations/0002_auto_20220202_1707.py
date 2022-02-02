# Generated by Django 2.2 on 2022-02-02 17:07

import api.models.base
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='household',
            name='interviewday',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MinValueValidator(31)]),
        ),
        migrations.AddField(
            model_name='household',
            name='interviewmonth',
            field=models.PositiveSmallIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MinValueValidator(12)]),
        ),
        migrations.AddField(
            model_name='household',
            name='interviewyear',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030), (2031, 2031), (2032, 2032), (2033, 2033), (2034, 2034), (2035, 2035), (2036, 2036), (2037, 2037), (2038, 2038), (2039, 2039), (2040, 2040), (2041, 2041), (2042, 2042), (2043, 2043), (2044, 2044), (2045, 2045), (2046, 2046), (2047, 2047), (2048, 2048), (2049, 2049), (2050, 2050), (993, 'Pertanyaan tidak diminta dalam survei ini (tidak ada skip logic) / Question not asked as part of this survey'), (994, 'Pertanyaan dilewati berdasarkan skip logic survei / Question skipped based on survey skip logic'), (995, 'Tidak Ada data / No data'), (996, 'Lainnya / Other'), (997, 'Tidak tahu / Do not know'), (998, 'Tidak sesuai / Not applicable'), (999, 'Menolak / Refused')], null=True, validators=[api.models.base.MinValueBCValidator(2000), api.models.base.MaxValueBCValidator(2050)]),
        ),
        migrations.AlterField(
            model_name='fgd',
            name='extbnd',
            field=models.PositiveSmallIntegerField(default=995, validators=[api.models.base.MinValueBCValidator(0), api.models.base.MaxValueBCValidator(100)]),
        ),
        migrations.AlterField(
            model_name='fgd',
            name='intbnd',
            field=models.PositiveSmallIntegerField(default=995, validators=[api.models.base.MinValueBCValidator(0), api.models.base.MaxValueBCValidator(100)]),
        ),
        migrations.AlterField(
            model_name='fgd',
            name='penaltyverbal',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Tidak / No'), (1, 'Ya / Yes'), (993, 'Pertanyaan tidak diminta dalam survei ini (tidak ada skip logic) / Question not asked as part of this survey'), (994, 'Pertanyaan dilewati berdasarkan skip logic survei / Question skipped based on survey skip logic'), (995, 'Tidak Ada data / No data'), (996, 'Lainnya / Other'), (997, 'Tidak tahu / Do not know'), (998, 'Tidak sesuai / Not applicable'), (999, 'Menolak / Refused')], default=995),
        ),
    ]