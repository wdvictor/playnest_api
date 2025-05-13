import logging
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from datetime import date
from base.models import Customer, Details, Sale
from rest_framework.test import APITestCase
from .test_utils import log_pass, log_fail, log_warning

class CustomerTestCase(APITestCase):

    def setUp(self):
        self.details1 = Details.objects.create(email="john@example.com", birthday=date(1990, 5, 10))
        self.customer1 = Customer.objects.create(name="John Doe", details=self.details1)

        self.details2 = Details.objects.create(email="jane@example.com", birthday=date(1995, 7, 20))
        self.customer2 = Customer.objects.create(name="Jane Smith", details=self.details2)

        self.url = reverse('get_all_customers')
        self.client.credentials(HTTP_X_API_KEY=settings.API_TOKEN)



    def test_get_all_customers(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        log_pass('[test_get_all_customers]')
        
        

    def test_get_all_customers_filter_by_name(self):
        response = self.client.post(self.url, {'filter': 'name', 'data': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')
        log_pass('[test_get_all_customers_filter_by_name]')
        

    def test_get_all_customers_filter_by_email(self):
        response = self.client.post(self.url, {'filter': 'email', 'data':'jane@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Jane Smith')
        log_pass('[test_get_all_customers_filter_by_email]')


    def test_filter_no_results(self):
        response = self.client.post(self.url, {'filter': 'name', 'data': 'Nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        log_pass('[test_filter_no_results]')


    def test_delete_customer(self):
        customer_id = self.customer1.id
        delete_url = reverse('delete_customer', args=[customer_id])
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.post(self.url)
        self.assertEqual(len(response.data), 1)
        log_pass('[test_delete_customer]')


class SaleTestCase(APITestCase):

    def setUp(self):
        self.details = Details.objects.create(email='jonh.doe@gmail.com1', birthday=date(1990, 5, 10))
        self.customer = Customer.objects.create(name="John Doe", details=self.details)
        self.sale = Sale.objects.create(customer_fk=self.customer, date=date.today(), amount=100.0)
        self.url = reverse('add_sale')
        self.client.credentials(HTTP_X_API_KEY=settings.API_TOKEN)

    def add_sale(self):
        self.sale = Sale.objects.create(customer_fk=self.customer, date=date.today(), amount=100.0)
        self.sale.save()
    

    def test_get_all_sales(self): #
        response = self.client.get(reverse('get_all_sales'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_pass('[test_all_sales]')

    def test_get_all_sales_no_data(self):
        try:
            self.sale.delete()
            response = self.client.get(reverse('get_all_sales'))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            log_pass('[test_all_sales_no_data]')
        except Exception as e:
            log_fail('[test_get_all_sales_no_data]')
            log_warning('[Exception]: {}'.format(e))

    def test_add_sale(self):#
        data = {
            'customer_fk': self.customer.id,
            'amount': 100.0,
            'date': date.today()
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        log_pass('[test_add_sale]')
        
    def test_add_sale_invalid_data(self):
        
        data = {
            'customer': self.customer.id,
            'amount': -50.0,  
            'date': date.today()
        }
        response = self.client.put(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        log_pass('[test_add_sale_invalid_data]')


    def test_total_sales_per_day(self):
        self.add_sale()
        response = self.client.get(reverse('total_sales_per_day'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_pass('[test_total_sales_per_day]')
    

    def test_total_sales_per_day_no_data(self):
        self.sale.delete()
        response = self.client.get(reverse('total_sales_per_day'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        log_pass('[test_total_sales_per_day_no_data]')


    def test_top_customer_by_volume(self):
        self.add_sale()
        response = self.client.get(reverse('top_customer_by_volume'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_pass('[test_top_customer_by_volume]')


    def test_top_customer_by_volume_no_data(self):
        self.sale.delete()
        response = self.client.get(reverse('top_customer_by_volume'), data=())
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        log_pass('[test_top_customer_by_volume]')


    def test_top_customer_by_avg_sale(self):
        self.add_sale()
        response = self.client.get(reverse('top_customer_by_avg_sale'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_pass('[test_top_customer_by_avg_sale]')


    def test_top_customer_by_avg_sale_no_data(self):
        self.sale.delete()
        response = self.client.get(reverse('top_customer_by_avg_sale'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        log_pass('[test_top_customer_by_avg_sale_no_data]')


    def test_customer_by_purchase_frequency(self):
        self.add_sale()
        response = self.client.get(reverse('customer_by_purchase_frequency'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        log_pass('[test_customer_by_purchase_frequency]')


    def test_customer_by_purchase_frequency_no_data(self):
        self.sale.delete()
        response = self.client.get(reverse('customer_by_purchase_frequency'))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        log_pass('[test_customer_by_purchase_frequency_no_data]')