# Generated by Django 3.2.8 on 2021-11-21 10:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrgStructure', '0014_reorganization_type_of_reorganization'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reorganization',
            options={'ordering': ['-date', 'ord_reason', 'type_of_reorganization'], 'verbose_name': 'реогранизацию', 'verbose_name_plural': 'Изменения структуры'},
        ),
        migrations.AlterUniqueTogether(
            name='reorganization',
            unique_together={('type_of_reorganization', 'date', 'ord_reason', 'note')},
        ),
        migrations.RemoveField(
            model_name='reorganization',
            name='type_reorganization',
        ),
        migrations.DeleteModel(
            name='TypeReorganization',
        ),
    ]
