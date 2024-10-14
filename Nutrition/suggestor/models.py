from django.db import models

class FoodItem(models.Model):
    name = models.CharField(max_length=100)
    calories = models.FloatField()
    carbohydrates = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    fibers = models.FloatField()
    
    def __str__(self):
        return self.name
