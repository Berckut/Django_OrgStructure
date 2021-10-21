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
        verbose_name='Вид реорганизации',
        related_name='reorganization',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    date = models.DateField(                                # Дата события
        verbose_name='Дата события',
        default=datetime.date.today,
    )
    ord_reason = models.ForeignKey(                         # Причина реорганизации (ОРД)
        ORD,
        verbose_name='Причина реорганизации (ОРД)',
        related_name='reorganization',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    note = models.CharField(                                # Описание события
        verbose_name='Описание события',
        max_length=250
    )

    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.type_reorganization}, {self.date.strftime("%Y.%m.%d")}, "{self.note}")')

    def __str__(self):
        return f'{self.date.strftime("%Y.%m.%d")} {self.note}'

    class Meta:
        verbose_name = 'реогранизацию'                          # Читабельное название модели, в единственном числе
        verbose_name_plural = 'Изменения структуры'             # Название модели в множественном числе
        ordering = [                                            # Сортировка
            '-date',
            'ord_reason',
            'type_reorganization',
        ]
        unique_together = (                                     # Комбинация полей, которая должна быть уникальной
            'type_reorganization',
            'date',
            'ord_reason',
            'note',
        )


# Подразделение
class OrgUnit(models.Model):
    current_name = models.CharField(                            # Текущее наименование (например, Общий отдел)
        verbose_name='Текущее наименование',
        max_length=200
    )
    current_short_name = models.CharField(                      # Текущая аббревиатура (например, ОО)
        verbose_name='Текущая аббривеатура',
        max_length=20,
        null=True,
        blank=True,
    )
    current_structure_code = models.CharField(                  # Текущий структруный код (например, 31-02)
        verbose_name='Текущий структурный код',
        max_length=50,
        null=True,
        blank=True,
    )
    date_creation = models.DateField(                           # Дата создания
        verbose_name='Дата создания',
        default=datetime.date.today,
    )
    reason_creation = models.ForeignKey(                        # Причина создания
        Reorganization,
        verbose_name='Причина создания',
        related_name='org_unit_creation',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_abolition = models.DateField(                          # Дата упразднения
        verbose_name='Дата упразднения',
        null=True,
        blank=True,
    )
    reason_abolition = models.ForeignKey(                       # Причина упразднения
        Reorganization,
        verbose_name='Причина упразднения',
        related_name='org_unit_abolition',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exist = models.BooleanField(                                # Подразделение существует или упразднено?
        verbose_name='Подразделение существует?',
    )

    def __repr__(self):
        result = f'{self.__class__.__name__}('

        if self.current_structure_code:
            result += f'{self.current_structure_code} '

        if self.current_short_name:
            result += f'{self.current_short_name}, '
        else:
            result += f'{self.current_name}, '

        result += f'{self.date_creation.strftime("%Y.%m.%d")}, {self.exist})'

        return result

    def __str__(self):
        return self.current_name

    class Meta:
        verbose_name = 'подразделение'                          # Читабельное название модели, в единственном числе
        verbose_name_plural = 'Подразделения'                   # Название модели в множественном числе
        ordering = [                                            # Сортировка
            'current_name',
            '-date_creation',
        ]


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
