# age_categories/models.py

from django.db import models

class AgeCategory(models.Model):
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
    min_age = models.IntegerField()
    max_age = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.gender}) {self.min_age}-{self.max_age} years"
