from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField


class Registration(models.Model):
    class Meta:
        db_table = 'registration_posv'

    name = models.CharField(max_length=100, blank=False, null=False)
    surname = models.CharField(max_length=100, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=False)

    vk = models.CharField(max_length=100, blank=False)
    tg = models.CharField(max_length=100, validators=[RegexValidator(r'^@.+')], blank=False)

    phone = PhoneNumberField(blank=False, null=False)
    university = models.CharField(max_length=300, blank=False, null=False)
    faculty = models.CharField(max_length=300, blank=False)
    group = models.CharField(max_length=20, default=None)

    class forTransfer(models.TextChoices):
        ODINTSOVO = 'Да, от Одинцово и обратно', 'Да, от Одинцово и обратно'
        PARKPOBEDY = 'Да, от Парка Победы и обратно', 'Да, от Парка Победы и обратно'
        NO = 'Не нужен', 'Не нужен'

    transfer = models.CharField(
        max_length=50,
        choices=forTransfer.choices,
        default=forTransfer.NO,
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
    )

    health_features = models.TextField(blank=True)


class Transfer(models.Model):
    class Meta:
        db_table = 'transfer_posv'

    name = models.CharField(max_length=100, blank=False)
    surname = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=False)

    email = models.EmailField(max_length=254, blank=False)
    vk = models.CharField(max_length=100, blank=False)
    tg = models.CharField(max_length=100, validators=[RegexValidator(r'^@.+')], blank=False)
    phone = PhoneNumberField(blank=False)


class Rasselenie(models.Model):
    class Meta:
        db_table = 'rasselenie_posv'

    name = models.CharField(max_length=100, blank=False)
    surname = models.CharField(max_length=100, blank=False)
    middle_name = models.CharField(max_length=100, blank=False)

    sex = models.CharField(max_length=2, choices=(('W', 'Women'), ('M', 'Men')), blank=False)
    vk = models.CharField(max_length=100, blank=False)
    tg = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'^@.+')],
        blank=False,
        unique=True
    )

    faculty = models.CharField(max_length=300, blank=False)
    group = models.CharField(max_length=50, blank=False)
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
    )

# class ListNames(models.Model):
#         listname = models.ForeignKey(Rasselenie, related_name='values')
#         personname = models.CharField(max_length=200, blank=True)
