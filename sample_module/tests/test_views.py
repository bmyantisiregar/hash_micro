import urllib.parse
from model_bakery import baker

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission, Group

from sample_module.models import Product
from modular_engine.models import InstalledModule

User = get_user_model()

class ProductViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        InstalledModule.objects.create(
            name='sample_module',
            description='sample module',
            landing_url='/products/'
        )
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.manager_group, created = Group.objects.get_or_create(name='manager')

        self.user.groups.add(self.manager_group)

        self.product = baker.make(Product)


    def test_product_list_view(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_create_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('product_add'))
        self.assertRedirects(response, '/accounts/login/?next=/products/add/')

    def test_product_create_view_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('product_add'))
        self.assertEqual(response.status_code, 200)

    def test_product_update_view_requires_login(self):
        update_url = reverse('product_update', args=[self.product.pk])
        response = self.client.get(update_url)
        expected_login_url = f'/accounts/login/?next={urllib.parse.quote(update_url)}'
        self.assertRedirects(response, expected_login_url)

    def test_product_delete_view_requires_login(self):
        delete_url = reverse('product_delete', args=[self.product.pk])
        response = self.client.get(delete_url)
        expected_login_url = f'/accounts/login/?next={urllib.parse.quote(delete_url)}'
        self.assertRedirects(response, expected_login_url)

