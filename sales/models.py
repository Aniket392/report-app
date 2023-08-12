from typing import Iterable, Optional
from django.db import models
from django.shortcuts import reverse
from .utils import generate_code
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.utils import timezone

# Create your models here.
class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    class Meta:
        verbose_name = ("Position")
        verbose_name_plural = ("Positions")

    def save(self, *args, **kwargs):
        self.price = self.product.price*self.quantity
        return super().save(*args, **kwargs)
    
    def get_sales_id(self):
        sales_id = self.sale_set.first()
        return sales_id.id

    def __str__(self):
        return f"id: {self.id}, product: {self.product.name}, quantity: {self.quantity}"
    
class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=True)
    position = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ("Sale")
        verbose_name_plural = ("Sales")

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()
        if self.created is None:
            self.created = timezone.now()
        return super().save(*args, **kwargs)
    
    def get_positions(self):
        return self.position.all()
    
    def get_absolute_url(self):
        return reverse("sales:detail", kwargs={"pk": self.pk})
    

    def __str__(self):
        return f"Sales for amount of ₹{self.total_price}"
    
class CSV(models.Model):
    file_name = models.CharField(max_length=120, null=True)
    csv_file = models.FileField(upload_to='csvs', null=True)
    activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = ("CSV")
        verbose_name_plural = ("CSVs")

    def __str__(self):
        return self.file_name

