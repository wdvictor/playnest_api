from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_Customers),
    path('add/', views.add_customer),
    path('delete/<int:customer_id>/', views.deleteCustumer),
    path('update/<int:customer_id>/', views.update_customer),
    

    
]