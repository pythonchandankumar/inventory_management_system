from django.db import models

# Create your models here.

class InventoryModel(models.Model):
    product_name = models.CharField(max_length=100)
    product_description = models.TextField()
    available_quantity = models.IntegerField()

    def __str__(self):
        return self.product_name
