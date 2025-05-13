from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_all_Customers),
    path('add/', views.add_customer),
    path('delete/<int:customer_id>/', views.delete_customer),
    path('update/<int:customer_id>/', views.update_customer),
    path('sale/list/', views.get_all_sales),
    path('sale/add/', views.add_sale),
    path('sale/total_sales_per_day/', views.total_sales_per_day),

    
]