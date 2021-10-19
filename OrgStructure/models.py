from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


# Организационно-распорядительный документ
class ORD(models.Model):
    number = models.CharField(max_length=20)    # Номер организационно-распорядительного документа
    date = models.DateField()                   # Дата документа
    name = models.CharField(max_length=200)     # Название документа

    def __str__(self):
        return f'{self.date.year}.{self.date.month}.{self.date.day} {self.number} {self.name}'


# Вид реорганизации
class TypeReorganization(models.Model):
    type_reorganization = models.CharField(max_length=100)  # Вид реорганизации

    def __str__(self):
        return self.type_reorganization


# Реорганизация
class Reorganization(models.Model):
    type_reorganization = models.ForeignKey(                # Вид реорганизации
        TypeReorganization,
        related_name='reorganization',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    date = models.DateField()                               # Дата события
    ord_reason = models.ForeignKey(                         # Причина реорганизации (ОРД)
        ORD,
        related_name='reorganization',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    note = models.CharField(max_length=200)                 # Описание события

    def __str__(self):
        return f'{self.date.year}.{self.date.month}.{self.date.day} {self.note}'


# Подразделение
class OrgUnit(models.Model):
    current_name = models.CharField(max_length=200)             # Текущее наименование (например, Общий отдел)
    current_short_name = models.CharField(                      # Текущая аббревиатура (например, ОО)
        max_length=20,
        null=True,
        blank=True,
    )
    current_structure_code = models.CharField(                  # Текущий структруный код (например, 31-02)
        max_length=50,
        null=True,
        blank=True,
    )
    date_creation = models.DateField()                          # Дата создания
    reason_creation = models.ForeignKey(                        # Причина создания
        Reorganization,
        related_name='org_unit_creation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_abolition = models.DateField(                          # Дата упразднения
        null=True,
        blank=True,
    )
    reason_abolition = models.ForeignKey(                       # Причина упразднения
        Reorganization,
        related_name='org_unit_abolition',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exist = models.BooleanField()                               # Подразделение существует или упразднено?

    def __str__(self):
        return self.current_name


# Структурная единица
class StructureUnit(MPTTModel):
    org_unit = models.ForeignKey(                           # Подразделение
        OrgUnit,
        related_name='structure_unit',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    name = models.CharField(max_length=200)                 # Наименование (например, Общий отдел)
    short_name = models.CharField(                          # Аббревиатура (например, ОО)
        max_length=20,
        null=True,
        blank=True,
    )
    structure_code = models.CharField(                      # Структруный код (например, 31-02)
        max_length=50,
        null=True,
        blank=True,
    )
    parent = TreeForeignKey(                                # Подчиняется
        'self',
        related_name='subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_creation = models.DateField()                      # Дата создания (присвоения наименования)
    reason_creation = models.ForeignKey(                    # Причина создания
        Reorganization,
        related_name='structure_unit_creation',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    date_excluding = models.DateField(                      # Дата исключения из структуры
        null=True,
        blank=True,
    )
    reason_excluding = models.ForeignKey(                   # Причина исключения
        Reorganization,
        related_name='structure_unit_excluding',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exist = models.BooleanField()                           # Дейтвующее наименование?

    def __str__(self):
        return self.name
