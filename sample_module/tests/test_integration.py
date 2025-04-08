from django.test import TestCase, Client
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from model_bakery import baker
from sample_module.models import Product
from modular_engine.models import InstalledModule


class ProductIntegrationTest(TestCase):
    def setUp(self):
        """Set up test data and users"""
        self.client = Client()

        InstalledModule.objects.create(
            name='sample_module',
            description='sample module',
            landing_url='/products/'
        )

        # Create user groups
        self.manager_group, _ = Group.objects.get_or_create(name='manager')
        self.user_group, _ = Group.objects.get_or_create(name='user')
        self.public_group, _ = Group.objects.get_or_create(name='public')

        # Create test users
        self.manager = User.objects.create_user(username='manager', password='password123')
        self.user = User.objects.create_user(username='user', password='password123')
        self.public_user = User.objects.create_user(username='public_user', password='password123')

        # Assign groups to users
        self.manager.groups.add(self.manager_group)
        self.user.groups.add(self.user_group)
        self.public_user.groups.add(self.public_group)

        # Create a sample product
        self.product = baker.make(Product)

    def test_product_list_view(self):
        """Public users should be able to view the product list"""
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_create_requires_login(self):
        """Unauthenticated users should be redirected to login when trying to create a product"""
        response = self.client.get(reverse('product_add'))
        self.assertRedirects(response, f'/accounts/login/?next={reverse("product_add")}')

    def test_manager_can_create_product(self):
        """Managers should be able to create products"""
        self.client.login(username='manager', password='password123')
        response = self.client.post(reverse('product_add'), {
            'name': 'New Product',
            'barcode': '123456',
            'price': 10.99,
            'stock': 5
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertTrue(Product.objects.filter(name='New Product').exists())

    def test_user_can_create_product(self):
        """Users (non-managers) should be able to create products"""
        self.client.login(username='user', password='password123')
        response = self.client.post(reverse('product_add'), {
            'name': 'User Product',
            'barcode': '789101',
            'price': 15.99,
            'stock': 8
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Product.objects.filter(name='User Product').exists())

    def test_public_cannot_create_product(self):
        """Public users should NOT be able to create products"""
        self.client.login(username='public_user', password='password123')
        response = self.client.post(reverse('product_add'), {
            'name': 'Public Product',
            'barcode': '111213',
            'price': 9.99,
            'stock': 2
        })
        self.assertEqual(response.status_code, 403)

    def test_manager_can_edit_product(self):
        """Managers should be able to edit products"""
        self.client.login(username='manager', password='password123')
        response = self.client.post(reverse('product_update', args=[self.product.pk]), {
            'name': 'Updated Product',
            'barcode': self.product.barcode,
            'price': self.product.price,
            'stock': self.product.stock
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'Updated Product')

    def test_user_can_edit_product(self):
        """Users should be able to edit products"""
        self.client.login(username='user', password='password123')
        response = self.client.post(reverse('product_update', args=[self.product.pk]), {
            'name': 'User Updated Product',
            'barcode': self.product.barcode,
            'price': self.product.price,
            'stock': self.product.stock
        })
        self.assertEqual(response.status_code, 302)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, 'User Updated Product')

    def test_public_cannot_edit_product(self):
        """Public users should NOT be able to edit products"""
        self.client.login(username='public_user', password='password123')
        response = self.client.post(reverse('product_update', args=[self.product.pk]), {
            'name': 'Hacked Product'
        })
        self.assertEqual(response.status_code, 403)

    def test_manager_can_delete_product(self):
        """Managers should be able to delete products"""
        self.client.login(username='manager', password='password123')
        response = self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())

    def test_user_cannot_delete_product(self):
        """Users should NOT be able to delete products"""
        self.client.login(username='user', password='password123')
        response = self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertEqual(response.status_code, 403)

    def test_public_cannot_delete_product(self):
        """Public users should NOT be able to delete products"""
        self.client.login(username='public_user', password='password123')
        response = self.client.post(reverse('product_delete', args=[self.product.pk]))
        self.assertEqual(response.status_code, 403)
