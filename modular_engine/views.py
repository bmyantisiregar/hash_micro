from django.shortcuts import render, redirect
from django.apps import apps
from django.core.management import call_command
from .models import InstalledModule

def module_list_view(request):
    installed_modules = InstalledModule.objects.values_list('name', flat=True)
    all_modules = [app for app in apps.get_app_configs() if hasattr(app, 'module_metadata')]
    return render(request, 'modular_engine/module_list.html', {
        'all_modules': all_modules,
        'installed_modules': installed_modules
    })

def install_module(request, app_name):
    app_config = apps.get_app_config(app_name)
    metadata = app_config.module_metadata

    InstalledModule.objects.get_or_create(
        name=app_name,
        defaults={'description': metadata['description'], 'landing_url': metadata['landing_url']}
    )
    call_command('makemigrations', app_config.label)
    call_command('migrate', app_config.label)
    return redirect('/products/')

def uninstall_module(request, app_name):
    InstalledModule.objects.filter(name=app_name).delete()
    return redirect('/module/')

def upgrade_module(request, app_name):
    app_config = apps.get_app_config(app_name.split('.')[-1])
    metadata = app_config.module_metadata
    call_command('makemigrations', app_config.label)
    call_command('migrate', app_config.label)
    return redirect(metadata['landing_url'])