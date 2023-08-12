from django.db import models

# Create your models here.
class Customer(models.Model):
    name  = models.CharField(max_length=20)
    logo  = models.ImageField(upload_to='customers', default='no_picture.png')

    class Meta:
        verbose_name = ("Customer")
        verbose_name_plural = ("Customers")

    def __str__(self):
        return str(self.name)
