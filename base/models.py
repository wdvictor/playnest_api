from django.db import models
from django.contrib.auth.models import User


class Details(models.Model):
    email = models.EmailField()
    birthday = models.DateField()


class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    details = models.OneToOneField(Details, on_delete=models.CASCADE)

class Sale(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='sales')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)