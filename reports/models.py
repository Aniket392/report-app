from django.db import models
from profiles.models import Profile
from django.shortcuts import reverse

# Create your models here.

class Report(models.Model):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='reports', blank=True)
    remarks = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = ("Report")
        verbose_name_plural = ("Reports")
        ordering = ("-created",)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("reports:detail", kwargs={"pk": self.pk})
    