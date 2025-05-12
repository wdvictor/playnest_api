from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllCustomers),
    path('add/', views.addCustomer),
    path('delete/<int:customer_id>/', views.deleteCustumer),

    
]