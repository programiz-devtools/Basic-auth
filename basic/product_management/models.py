# myapp/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return self.name

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    def __str__(self):
        return f'{self.quantity} of {self.product_name}'
    

