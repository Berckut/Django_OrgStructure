from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin

# Register your models here.

admin.site.register(models.ORD)
admin.site.register(models.TypeReorganization)
admin.site.register(models.Reorganization)
admin.site.register(models.OrgUnit)
admin.site.register(models.StructureUnit, MPTTModelAdmin)
