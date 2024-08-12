from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField


class Registration(models.Model):
    full_name = models.CharField(max_length=300)
    vk = models.CharField(max_length=100)
    tg = models.CharField(max_length=100, validators=[RegexValidator(r'^@.+')])
    phone = PhoneNumberField()
    university = models.CharField(max_length=300)
    op = models.CharField(max_length=300)
    course = models.CharField(max_length=100)
    transfer = models.CharField(max_length=100)
    health_features = models.TextField(blank=True)


