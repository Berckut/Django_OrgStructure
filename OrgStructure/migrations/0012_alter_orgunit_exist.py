# Generated by Django 3.2.8 on 2021-10-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrgStructure', '0011_auto_20211021_2312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orgunit',
            name='exist',
            field=models.BooleanField(default=True, verbose_name='Подразделение существует?'),
        ),
    ]