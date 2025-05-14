import uuid
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from datetime import date
from base.models import Customer, Details, Sale
from rest_framework.test import APITestCase
from .test_utils import log_pass, log_fail, log_warning
from django.contrib.auth.models import User

class CustomerTestCase(APITestCase):

    def setUp(self):
        try:
            
            self.details1 = Details.objects.create(email="john@example.com", birthday=date(1990, 5, 10))            
            self.user1 = User.objects.create_user(username=f'joao_{uuid.uuid4().hex[:6]}', email='joao@example.com', password='senha123')
            self.customer1 = Customer.objects.create(name="John Doe", details=self.details1, user=self.user1)

            self.details2 = Details.objects.create(email="jane@example.com", birthday=date(1995, 7, 20))
            self.user2 = User.objects.create_user(username=f'joao_{uuid.uuid4().hex[:6]}', email='marcos@example.com', password='senha123')
            self.customer2 = Customer.objects.create(name="marcos Smith", details=self.details2, user=self.user2)

            self.url = reverse('get_all_users')
            self.client.credentials(HTTP_X_API_KEY=settings.API_TOKEN)  # type: ignore
        except Exception as e:
            log_fail('[setUp]')
            log_warning('[Exception]: {}'.format(e))



    def test_get_all_customers(self):
        try:
            response = self.client.post(self.url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2) # type: ignore
            log_pass('[test_get_all_customers]')
        except Exception as e:
            log_fail('[test_get_all_customers]')
            log_warning('[Exception]: {}'.format(e))



    def test_get_all_customers_filter_by_name(self):
        try:
            response = self.client.post(self.url, {'filter': 'name', 'data': 'John'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1) # type: ignore 
            self.assertEqual(response.data[0]['name'], 'John Doe') # type: ignore
            log_pass('[test_get_all_customers_filter_by_name]')
        except Exception as e:
            log_fail('[test_get_all_customers_filter_by_name]')
            log_warning('[Exception]: {}'.format(e))



    def test_get_all_customers_filter_by_email(self):
        try:
            response = self.client.post(self.url, {'filter': 'email', 'data': 'jane@example.com'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 1) # type: ignore
            log_pass('[test_get_all_customers_filter_by_email]')
        except Exception as e:
            log_fail('[test_get_all_customers_filter_by_email]')
            log_warning('[Exception]: {}'.format(e))



    def test_filter_no_results(self):
        try:
            response = self.client.post(self.url, {'filter': 'name', 'data': 'Nonexistent'})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 0) # type: ignore
            log_pass('[test_filter_no_results]')
        except Exception as e:
            log_fail('[test_filter_no_results]')
            log_warning('[Exception]: {}'.format(e))



    def test_delete_user(self):
        try:
            user_id = self.customer1.id # type: ignore 
            delete_url = reverse('delete_user', args=[user_id])
            response = self.client.delete(delete_url)
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
            response = self.client.post(self.url)
            self.assertEqual(len(response.data), 1) # type: ignore
            log_pass('[test_delete_user]')
        except Exception as e:
            log_fail('[test_delete_user]')
            log_warning('[Exception]: {}'.format(e))


class SaleTestCase(APITestCase):

    def setUp(self):
        try:
            self.user = User.objects.create_user(username=f'joao_{uuid.uuid4().hex[:6]}', password='senha123')   
            self.details = Details.objects.create(email='jonh.doe@gmail.com1', birthday=date(1990, 5, 10))
            self.customer = Customer.objects.create(name="John Doe", details=self.details, user=self.user)
            self.sale = Sale.objects.create(user_id=self.customer, date=date.today(), amount=100.0)
            self.url = reverse('add_sale')
            self.client.credentials(HTTP_X_API_KEY=settings.API_TOKEN) # type: ignore
        except Exception as e:
            log_fail('[setUp]')
            log_warning('[Exception]: {}'.format(e))



    def add_sale(self):
        try:
            self.sale = Sale.objects.create(user_id=self.customer, date=date.today(), amount=100.0)
            self.sale.save()
        except Exception as e:
            log_fail('[add_sale]')
            log_warning('[Exception]: {}'.format(e))



    def test_get_all_sales(self):
        try:
            response = self.client.get(reverse('get_all_sales'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            log_pass('[test_all_sales]')
        except Exception as e:
            log_fail('[test_get_all_sales]')
            log_warning('[Exception]: {}'.format(e))



    def test_get_all_sales_no_data(self):
        try:
            self.sale.delete()
            response = self.client.get(reverse('get_all_sales'))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            log_pass('[test_all_sales_no_data]')
        except Exception as e:
            log_fail('[test_get_all_sales_no_data]')
            log_warning('[Exception]: {}'.format(e))



    def test_add_sale(self):
        try:
            data = {
                'user_id': self.customer.id, # type: ignore
                'amount': 100.0,
                'date': date.today()
            }
            response = self.client.put(self.url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            log_pass('[test_add_sale]')
        except Exception as e:
            log_fail('[test_add_sale]')
            log_warning('[Exception]: {}'.format(e))



    def test_add_sale_invalid_data(self):
        try:
            data = {
                'user': self.customer.id, # type: ignore
                'amount': -50.0,
                'date': date.today()
            }
            response = self.client.put(self.url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            log_pass('[test_add_sale_invalid_data]')
        except Exception as e:
            log_fail('[test_add_sale_invalid_data]')
            log_warning('[Exception]: {}'.format(e))



    def test_total_sales_per_day(self):
        try:
            self.add_sale()
            response = self.client.get(reverse('total_sales_per_day'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            log_pass('[test_total_sales_per_day]')
        except Exception as e:
            log_fail('[test_total_sales_per_day]')
            log_warning('[Exception]: {}'.format(e))



    def test_total_sales_per_day_no_data(self):
        try:
            self.sale.delete()
            response = self.client.get(reverse('total_sales_per_day'))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            log_pass('[test_total_sales_per_day_no_data]')
        except Exception as e:
            log_fail('[test_total_sales_per_day_no_data]')
            log_warning('[Exception]: {}'.format(e))



    def test_top_user_by_volume(self):
        try:
            self.add_sale()
            response = self.client.get(reverse('top_user_by_volume'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            log_pass('[test_top_user_by_volume]')
        except Exception as e:
            log_fail('[test_top_user_by_volume]')
            log_warning('[Exception]: {}'.format(e))



    def test_top_user_by_volume_no_data(self):
        try:
            self.sale.delete()
            response = self.client.get(reverse('top_user_by_volume'), data=())
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            log_pass('[test_top_user_by_volume]')
        except Exception as e:
            log_fail('[test_top_user_by_volume]')
            log_warning('[Exception]: {}'.format(e))



    def test_top_user_by_avg_sale(self):
        try:
            self.add_sale()
            response = self.client.get(reverse('top_user_by_avg_sale'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            log_pass('[test_top_user_by_avg_sale]')
        except Exception as e:
            log_fail('[test_top_user_by_avg_sale]')
            log_warning('[Exception]: {}'.format(e))



    def test_top_user_by_avg_sale_no_data(self):
        try:
            self.sale.delete()
            response = self.client.get(reverse('top_user_by_avg_sale'))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            log_pass('[test_top_user_by_avg_sale_no_data]')
        except Exception as e:
            log_fail('[test_top_user_by_avg_sale_no_data]')
            log_warning('[Exception]: {}'.format(e))



    def test_top_user_by_purchase_frequency(self):
        try:
            self.add_sale()
            response = self.client.get(reverse('top_user_by_purchase_frequency'))
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            log_pass('[top_user_by_purchase_frequency]')
        except Exception as e:
            log_fail('[test_top_user_by_purchase_frequency]')
            log_warning('[Exception]: {}'.format(e))



    def test_top_user_by_purchase_frequency_no_data(self):
        try:
            self.sale.delete()
            response = self.client.get(reverse('top_user_by_purchase_frequency'))
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
            log_pass('[test_top_user_by_purchase_frequency_no_data]')
        except Exception as e:
            log_fail('[test_top_user_by_purchase_frequency_no_data]')
            log_warning('[Exception]: {}'.format(e))