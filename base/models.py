from django.db import models


class Details(models.Model):
    email = models.EmailField()
    birthday = models.DateField()


class Customer(models.Model):
    name = models.CharField(max_length=100)
    details = models.OneToOneField(Details, on_delete=models.CASCADE)

class Sale(models.Model):
    customer_fk = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)