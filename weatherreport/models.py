from django.db import models

# Create your models here.

# This is the design for the backend database. It is very simple and only has one model. 

class City(models.Model):
    name = models.CharField(max_length=32)
    temperature = models.FloatField(null=True, blank=True)
    conditions = models.CharField(max_length=100, null=True, blank=True)
    icon = models.CharField(max_length=32, default="none.png")

    def __str__(self):
        return self.name