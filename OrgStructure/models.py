from django.db import models
import datetime
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class ORD(models.Model):
    """
    Модель "Организационно-распорядительный документ"
    """
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


class Reorganization(models.Model):
    """
    Модель "Реорганизация"
    """

    class TypeOfReorganization(models.TextChoices):
        """
        Вид реорганизации
        """
        CREATION = 'cr', 'Создание'
        ABOLITION = 'ab', 'Упразднение'
        ALLOCATION = 'al', 'Выделение'      # выделение - подразделения А возникает отдел Б, при этом существуют оба
        TRANSFORMATION = 'tr', 'Преобразование'     # изменение свойств, в т.ч., переименование
        JOINING = 'jo', 'Присоединение'     # к подразделению А присоединяется Б, при этом Б перестает существовать
        PARTITION = 'pa', 'Разделение'      # из отдела А образуются отделы Б и В, при этом А перестает существовать
        MERGING = 'me', 'Слияние'       # из отделов А и Б возникает отдел В, при этом А и Б перестают существовать

    type_of_reorganization = models.CharField(      # Вид реорганизации
        choices=TypeOfReorganization.choices,
        max_length=2,
        verbose_name='Вид реорганизации',
        null=False,
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
                f'{self.type_of_reorganization}, {self.date.strftime("%Y.%m.%d")}, "{self.note}")')

    def __str__(self):
        return f'{self.date.strftime("%Y.%m.%d")} {self.note}'

    class Meta:
        verbose_name = 'реогранизацию'                          # Читабельное название модели, в единственном числе
        verbose_name_plural = 'Изменения структуры'             # Название модели в множественном числе
        ordering = [                                            # Сортировка
            '-date',
            'ord_reason',
            'type_of_reorganization',
        ]
        unique_together = (                                     # Комбинация полей, которая должна быть уникальной
            'type_of_reorganization',
            'date',
            'ord_reason',
            'note',
        )


class OrgUnit(models.Model):
    """
    Модель "Подразделение"
    """
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
        default=True,
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


class StructureUnit(MPTTModel):
    """
    Модель "Структурная единица"
    """
    org_unit = models.ForeignKey(                           # Подразделение
        OrgUnit,
        verbose_name='Подразделение',
        related_name='structure_unit',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(                                # Наименование (например, Общий отдел)
        verbose_name='Наименование',
        max_length=200
    )
    short_name = models.CharField(                          # Аббревиатура (например, ОО)
        verbose_name='Аббревиатура',
        max_length=20,
        null=True,
        blank=True,
    )
    structure_code = models.CharField(                      # Структруный код (например, 31-02)
        verbose_name='Структруный код',
        max_length=50,
        null=True,
        blank=True,
    )
    parent = TreeForeignKey(                                # Подчиняется
        'self',
        verbose_name='Подчиняется',
        related_name='subject',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    date_creation = models.DateField(                       # Дата ввода в структуру (присвоения наименования)
        verbose_name='Дата ввода в структуру',
        default=datetime.date.today,
    )
    reason_creation = models.ForeignKey(                    # Причина ввода
        Reorganization,
        verbose_name='Причина ввода',
        related_name='structure_unit_creation',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
    )
    date_excluding = models.DateField(                      # Дата исключения из структуры
        verbose_name='Дата исключения из структуры',
        null=True,
        blank=True,
    )
    reason_excluding = models.ForeignKey(                   # Причина исключения
        Reorganization,
        verbose_name='Причина исключения',
        related_name='structure_unit_excluding',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    exist = models.BooleanField(                            # Дейтвующее наименование?
        verbose_name='Действующее?',
        default=True,
    )

    def __repr__(self):
        result = f'{self.__class__.__name__}('

        if self.structure_code:
            result += f'{self.structure_code} '

        if self.short_name:
            result += f'{self.short_name}, '
        else:
            result += f'{self.name}, '

        result += f'{self.date_creation.strftime("%Y.%m.%d")}, {self.exist}'

        if self.parent:
            result += f', {self.parent}'

        result += ')'

        return result

    def __str__(self):
        if self.structure_code:
            return f'{self.structure_code} {self.name}'

        return self.name

    class Meta:
        verbose_name = 'структурную единицу'  # Читабельное название модели, в единственном числе
        verbose_name_plural = 'Структура'  # Название модели в множественном числе

    class MPTTMeta:
        order_insertion_by = [                              # Сортировка узлов дерева подразделений
            'structure_code',
            'name',
        ]
