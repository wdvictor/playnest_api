import logging
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from datetime import date
from base.models import Customer, Details
from rest_framework.test import APITestCase
logger = logging.getLogger(__name__)
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
        print('-->[test_get_all_customers] [Done]')
        
        

    def test_get_all_customers_filter_by_name(self):
        response = self.client.post(self.url, {'filter': 'name', 'data': 'John'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')
        print('-->[test_get_all_customers_filter_by_name] [Done]')
        

    def test_get_all_customers_filter_by_email(self):
        response = self.client.post(self.url, {'filter': 'email', 'data':'jane@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Jane Smith')
        print('-->[test_get_all_customers_filter_by_email] [Done]')


    def test_filter_no_results(self):
        response = self.client.post(self.url, {'filter': 'name', 'data': 'Nonexistent'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        print('-->[test_filter_no_results] [Done]')

