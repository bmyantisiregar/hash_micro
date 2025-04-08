from django.test import TestCase
from model_bakery import baker
from sample_module.forms import ProductForm
from sample_module.models import Product


class ProductFormTest(TestCase):
    def test_valid_product_form(self):
        product = baker.prepare(Product)  # create an unsaved product instance with random data
        form_data = {
            'name': product.name,
            'barcode': product.barcode,
            'price': product.price,
            'stock': product.stock,
        }
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_product_form(self):
        # Missing all fields
        form = ProductForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('barcode', form.errors)
        self.assertIn('price', form.errors)
        self.assertIn('stock', form.errors)
