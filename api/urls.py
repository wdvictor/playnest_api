from atexit import register
from django.urls import path
from . import views


urlpatterns = [
    path('login/',  views.login_user, name='login'),
    path('register/', views.register_user, name='register_user'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('update_user/<int:user_id>/', views.update_user, name='update_user'),
    path('sale/get_all_sales/', views.get_all_sales, name='get_all_sales'),
    path('sale/add_sale/', views.add_sale, name='add_sale'),
    path('sale/total_sales_per_day/', views.total_sales_per_day, name='total_sales_per_day'),
    path('sale/top_user_by_volume/', views.top_user_by_volume, name='top_user_by_volume'),
    path('sale/top_user_by_avg_sale/', views.top_user_by_avg_sale, name='top_user_by_avg_sale'),
    path('sale/top_user_by_purchase_frequency/', views.top_user_by_purchase_frequency, name='top_user_by_purchase_frequency'),
    path('sale/get_all_users_data/', views.get_all_users_data, name='get_all_users_data'),


  
]