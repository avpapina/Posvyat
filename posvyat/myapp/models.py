from django.db import models

class Registration(models.Model):
    full_name = models.CharField(max_length=100)
    vk = models.CharField(max_length=100)
    tg = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    university = models.CharField(max_length=100)
    op = models.CharField(max_length=100)
    course = models.CharField(max_length=10)
    transfer = models.BooleanField(default=False)
    health_features = models.TextField(blank=True)

    def __str__(self):
        return self.full_name
