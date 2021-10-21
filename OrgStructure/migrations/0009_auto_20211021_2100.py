# Generated by Django 3.2.8 on 2021-10-21 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrgStructure', '0008_auto_20211021_1052'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='typereorganization',
            options={'ordering': ['type_reorganization'], 'verbose_name': 'Вид реорганизации', 'verbose_name_plural': 'Виды реорганизации'},
        ),
        migrations.AddField(
            model_name='typereorganization',
            name='description',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='typereorganization',
            name='type_reorganization',
            field=models.CharField(max_length=100, unique=True, verbose_name='Вид реорганизации'),
        ),
    ]
