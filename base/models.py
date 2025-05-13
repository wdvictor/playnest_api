from django.db import models


class Details(models.Model):
    email = models.EmailField()
    birthday = models.DateField()


class Customer(models.Model):
    name = models.CharField(max_length=100)
    details = models.OneToOneField(Details, on_delete=models.CASCADE)



