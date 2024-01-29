from django.db import models


class Part(models.Model):
    serial_number = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()
    location = models.JSONField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100, null=True)
