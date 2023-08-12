from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=20)
    image = models.ImageField(upload_to='products', default='no_picture.png')
    price = models.FloatField(help_text='in Rupees ₹')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return f"{self.name}-{self.created.strftime('%d%m%Y')}"
