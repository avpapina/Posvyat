from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField


class Registration(models.Model):

    name = models.CharField(max_length=100, blank=False, null=False)
    surname = models.CharField(max_length=100, blank=False, null=False)
    middle_name = models.CharField(max_length=100, blank=False)

    vk = models.CharField(max_length=100, blank=False)
    tg = models.CharField(max_length=100, validators=[RegexValidator(r'^@.+')], blank= False)

    phone = PhoneNumberField(blank=False, null=False)
    university = models.CharField(max_length=300, blank=False, null=False)
    faculty = models.CharField(max_length=300, blank=False)
    group = models.CharField(max_length=20)

    class Transfer(models.TextChoices):

        ODINTSOVO = 'OD', 'Да, от Одинцово и обратно'
        PARKPOBEDY = 'PP', 'Да, от Парка Победы и обратно'
        NO = 'NO', 'Не нужен'

    transfer = models.CharField(
        max_length=2,
        choices=Transfer.choices,
        default=Transfer.NO,
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


