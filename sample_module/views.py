from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Product
from .mixins import RolePermissionMixin


class ProductListView(ListView):
    model = Product
    template_name = 'sample_module/product_list.html'
    context_object_name = 'products'


class ProductCreateView(LoginRequiredMixin, RolePermissionMixin, CreateView):
    model = Product
    fields = ['name', 'barcode', 'price', 'stock']
    template_name = 'sample_module/product_form.html'
    success_url = '/products/'
    required_permission = 'add_product'


class ProductUpdateView(LoginRequiredMixin, RolePermissionMixin, UpdateView):
    model = Product
    fields = ['name', 'barcode', 'price', 'stock']
    template_name = 'sample_module/product_form.html'
    success_url = '/products/'
    required_permission = 'change_product'


class ProductDeleteView(LoginRequiredMixin, RolePermissionMixin, DeleteView):
    model = Product
    template_name = 'sample_module/product_confirm_delete.html'
    success_url = '/products/'
    required_permission = 'delete_product'
