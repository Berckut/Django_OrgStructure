from django.db import models
import datetime
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


# Организационно-распорядительный документ
class ORD(models.Model):
    number = models.CharField(                  # Номер документа
        verbose_name='Номер документа',
        max_length=20,
        null=True,
        blank=True,
    )
    date = models.DateField(                    # Дата документа
        verbose_name='Дата документа',
        default=datetime.date.today,
    )
    name = models.CharField(                    # Название документа
        verbose_name='Название документа',
        max_length=200,
    )

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.date.strftime("%Y.%m.%d")}, {self.number}, "{self.name}")')

    def __str__(self):
        if self.number:
            return f'{self.date.strftime("%Y.%m.%d")} № {self.number} "{self.name}"'
        else:
            return f'{self.date.strftime("%Y.%m.%d")} {self.name}'

    class Meta:
        verbose_name = 'ОРД'                                # Читабельное название модели, в единственном числе
        verbose_name_plural = 'ОРД'                         # Название модели в множественном числе
        ordering = ['-date', '-number']                     # Сортировка
        unique_together = ('number', 'date', 'name')        # Комбинация полей, которая должна быть уникальной


# Вид реорганизации
class TypeReorganization(models.Model):
    type_reorganization = models.CharField(                 # Вид реорганизации
        verbose_name='Вид реорганизации',
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    description = models.CharField(                 # Описание
        verbose_name='Описание',
        max_length=250,
        null=True,
        blank=True,
    )

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.type_reorganization})')

    def __str__(self):
        return self.type_reorganization

    class Meta:
        verbose_name = 'Вид реорганизации'                  # Читабельное название модели, в единственном числе
        verbose_name_plural = 'Виды реорганизации'          # Название модели в множественном числе
        ordering = ['type_reorganization']                  # Сортировка


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
