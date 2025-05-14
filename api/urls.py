from django.urls import path
from . import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('get_all_customers/', views.get_all_customers, name='get_all_customers'),
    path('add_customer/', views.add_customer, name='add_customer'),
    path('delete_customer/<int:customer_id>/', views.delete_customer, name='delete_customer'),
    path('update_customer/<int:customer_id>/', views.update_customer, name='update_customer'),
    path('sale/get_all_sales/', views.get_all_sales, name='get_all_sales'),
    path('sale/add_sale/', views.add_sale, name='add_sale'),
    path('sale/total_sales_per_day/', views.total_sales_per_day, name='total_sales_per_day'),
    path('sale/top_customer_by_volume/', views.top_customer_by_volume, name='top_customer_by_volume'),
    path('sale/top_customer_by_avg_sale/', views.top_customer_by_avg_sale, name='top_customer_by_avg_sale'),
    path('sale/top_customer_by_purchase_frequency/', views.top_customer_by_purchase_frequency, name='top_customer_by_purchase_frequency'),
    path('sale/get_all_customers_data/', views.get_all_customers_data, name='get_all_customers_data'),


  
]