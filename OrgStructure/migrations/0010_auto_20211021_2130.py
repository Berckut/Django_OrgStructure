# Generated by Django 3.2.8 on 2021-10-21 14:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('OrgStructure', '0009_auto_20211021_2100'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reorganization',
            options={'ordering': ['-date', 'ord_reason', 'type_reorganization'], 'verbose_name': 'реогранизацию', 'verbose_name_plural': 'Изменения структуры'},
        ),
        migrations.AlterField(
            model_name='reorganization',
            name='date',
            field=models.DateField(default=datetime.date.today, verbose_name='Дата события'),
        ),
        migrations.AlterField(
            model_name='reorganization',
            name='note',
            field=models.CharField(max_length=250, verbose_name='Описание события'),
        ),
        migrations.AlterField(
            model_name='reorganization',
            name='ord_reason',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reorganization', to='OrgStructure.ord', verbose_name='Причина реорганизации (ОРД)'),
        ),
        migrations.AlterField(
            model_name='reorganization',
            name='type_reorganization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reorganization', to='OrgStructure.typereorganization', verbose_name='Вид реорганизации'),
        ),
        migrations.AlterUniqueTogether(
            name='reorganization',
            unique_together={('type_reorganization', 'date', 'ord_reason', 'note')},
        ),
    ]
