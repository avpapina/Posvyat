from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField


class Registration(models.Model):
    class Meta:
        db_table = 'registration_posv'
        verbose_name = "Регистрация"
        verbose_name_plural = "Регистрации"

    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    surname = models.CharField(max_length=100, blank=False, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=False, verbose_name='Отчество')

    vk = models.CharField(max_length=100, blank=False, verbose_name='VK')
    tg = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^@.+')],
        blank=False,
        verbose_name='Telegram'
    )

    phone = PhoneNumberField(
        blank=False,
        null=False,
        verbose_name='Телефон',
        unique=True
    )
    bday = models.DateField(blank=False, verbose_name='Дата рождения')
    sex = models.CharField(
        max_length=10,
        choices=(('Женский', 'Woman'), ('Мужской', 'Man')),
        blank=False,
        verbose_name='Пол'
    )
    university = models.CharField(max_length=300, blank=False, verbose_name='Университет')
    faculty = models.CharField(max_length=300, blank=False, verbose_name='Факультет')
    group = models.CharField(max_length=20, default=None, verbose_name='Группа')

    class forTransfer(models.TextChoices):
        ODINTSOVO = 'Да, от Одинцово и обратно', 'Да, от Одинцово и обратно'
        PARKPOBEDY = 'Да, от Парка Победы и обратно', 'Да, от Парка Победы и обратно'
        NO = 'Не нужен', 'Не нужен'

    transfer = models.CharField(
        max_length=50,
        choices=forTransfer.choices,
        default=forTransfer.NO,
        verbose_name='Трансфер'
    )

    course_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    course = models.IntegerField(
        choices=course_choices,
        default=1,
        verbose_name='Курс'
    )

    health_features = models.TextField(blank=True, verbose_name='Особенности здоровья')

    def __str__(self):
        return f'<{self.surname} {self.name} {self.group}>'


class Transfer(models.Model):
    class Meta:
        db_table = 'transfer_posv'
        verbose_name = 'Трансфер'
        verbose_name_plural = 'Трансфер'

    TIMES = (
        ('15:15', '15:15'),
        ('15:35', '15:35'),
    )

    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    surname = models.CharField(max_length=100, blank=False, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=False, verbose_name='Отчество')

    email = models.EmailField(max_length=254, blank=False)
    vk = models.CharField(max_length=100, blank=False, verbose_name='VK')
    tg = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^@.+')],
        blank=False,
        verbose_name='Telegram'
    )
    phone = PhoneNumberField(
        blank=False,
        null=False,
        verbose_name='Телефон',
        unique=True
    )
    _from = models.CharField(
        max_length=15,
        choices=(('Парк Победы', 'Парк Победы'), ('Одинцово', 'Одинцово')),
        blank=False,
        verbose_name='Откуда трансфер'
    )
    departure_time = models.CharField(
        max_length=30,
        choices=TIMES,
        blank=False,
        default=None,
        verbose_name='Время отправления'
    )

    def __str__(self):
        return f'<{self.surname} {self.name}>'


class Rasselenie(models.Model):
    class Meta:
        db_table = 'rasselenie_posv'
        verbose_name = 'Расселение'
        verbose_name_plural = 'Расселение'

    name = models.CharField(max_length=100, blank=False, verbose_name='Имя')
    surname = models.CharField(max_length=100, blank=False, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=100, blank=False, verbose_name='Отчество')

    vk = models.CharField(max_length=100, blank=False, verbose_name='VK')
    tg = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^@.+')],
        blank=False,
        unique=True,
        verbose_name='Telegram'
    )
    phone = PhoneNumberField(
        blank=False,
        null=False,
        verbose_name='Телефон',
        unique=True
    )

    program = models.CharField(
        max_length=300,
        blank=False,
        verbose_name='Образовательная программа'
    )
    group = models.CharField(max_length=50, blank=False, verbose_name='Группа')
    course_choices = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    course = models.IntegerField(
        choices=course_choices,
        default=1,
        verbose_name='Курс'
    )
    people_custom = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Сожители'
    )

    def __str__(self):
        return f'<{self.surname} {self.name} {self.group}>'
# class ListNames(models.Model):
#         listname = models.ForeignKey(Rasselenie, related_name='values')
#         personname = models.CharField(max_length=200, blank=True
