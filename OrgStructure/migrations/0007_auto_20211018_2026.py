# Generated by Django 3.2.8 on 2021-10-18 13:26

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('OrgStructure', '0006_alter_reorganization_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='structureunit',
            name='date_excluding',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='structureunit',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subject', to='OrgStructure.structureunit'),
        ),
        migrations.AlterField(
            model_name='structureunit',
            name='reason_excluding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='structure_unit_excluding', to='OrgStructure.reorganization'),
        ),
        migrations.AlterField(
            model_name='structureunit',
            name='short_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='structureunit',
            name='structure_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
