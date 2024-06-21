from django.db import models

from inventory.models import InventoryModel
# Create your models here.

class CustomerModel(models.Model):
    customer = models.CharField(max_length=100)
    contact = models.IntegerField()

    def __str__(self):
        return self.customer


class SalesModel(models.Model):
    order_no = models.IntegerField(primary_key=True)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    product = models.ForeignKey(InventoryModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer

    def save(self, *args, **kwargs):
        if self.pk is None:
            # New record
            self.product.available_quantity -= self.quantity
        else:
            # Existing record
            old_quantity = SalesModel.objects.get(pk=self.pk).quantity
            self.product.available_quantity -= self.quantity - old_quantity
        self.product.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.product.available_quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)
