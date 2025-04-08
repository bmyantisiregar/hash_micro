from django.urls import path
from . import views

urlpatterns = [
    path('module/', views.module_list_view, name='module_list'),
    path('module/install/<str:app_name>/', views.install_module, name='install_module'),
    path('module/uninstall/<str:app_name>/', views.uninstall_module, name='uninstall_module'),
    path('module/upgrade/<str:app_name>/', views.upgrade_module, name='upgrade_module'),
]
