from django.db import models

# Create your models here.

class Item(models.Model):
    outfit = models.ImageField(upload_to="images")
    bottoms = models.ImageField(upload_to="images")
    cover = models.ImageField(upload_to="images")
    shoes = models.ImageField(upload_to="images")
    rainproof = models.BooleanField()
    smart = models.BooleanField()
    lastworn = models.DateField(null=True, blank=True)

