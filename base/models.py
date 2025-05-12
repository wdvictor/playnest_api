from django.db import models


class Item(models.Model):

    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)



class Details(models.Model):
    
    email = models.EmailField()
    birthday = models.DateField()


class Customer(models.Model):

    name = models.CharField(max_length=100)
    details = models.OneToOneField(Details, on_delete=models.CASCADE)



