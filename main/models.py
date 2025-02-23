from django.db import models

# Create your models here.
class formcontainer(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone_number=models.IntegerField(12)
    message=models.CharField(max_length=300)
