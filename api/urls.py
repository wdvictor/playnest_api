from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllCustomers),
    path('add/', views.addCustomer)
]