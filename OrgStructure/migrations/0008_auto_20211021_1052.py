# Generated by Django 3.2.8 on 2021-10-21 03:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrgStructure', '0007_auto_20211018_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ord',
            options={'ordering': ['-date', '-number'], 'verbose_name': 'ОРД', 'verbose_name_plural': 'ОРД'},
        ),
        migrations.AlterField(
            model_name='ord',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата документа'),
        ),
        migrations.AlterField(
            model_name='ord',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Название документа'),
        ),
        migrations.AlterField(
            model_name='ord',
            name='number',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер документа'),
        ),
        migrations.AlterUniqueTogether(
            name='ord',
            unique_together={('number', 'date', 'name')},
        ),
    ]