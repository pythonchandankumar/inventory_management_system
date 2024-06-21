from django.db import models

from supplier.models import SupplierModel
from inventory.models import InventoryModel
# Create your models here.

class NewStockModel(models.Model):
    order_no = models.IntegerField(primary_key=True)
    sku = models.ForeignKey(InventoryModel, on_delete=models.CASCADE)
    supplier = models.ForeignKey(SupplierModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()
    total_price = models.IntegerField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sku.product_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # New record
            self.sku.available_quantity += self.quantity
        else:
            # Existing record, calculate the difference
            original_record = NewStockModel.objects.get(pk=self.pk)
            quantity_difference = self.quantity - original_record.quantity
            self.sku.available_quantity += quantity_difference
        
        self.sku.save()  # Save the updated available quantity
        super().save(*args, **kwargs)  # Proceed with the save operation

    def delete(self, *args, **kwargs):
        self.sku.available_quantity -= self.quantity
        self.sku.save()
        super().delete(*args, **kwargs)