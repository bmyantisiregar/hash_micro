from django.test import TestCase
from django.urls import reverse
from django.apps import apps
from modular_engine.models import InstalledModule


class ModularEngineIntegrationTests(TestCase):
    def test_module_list_view_shows_all_modules_and_installed_status(self):
        InstalledModule.objects.create(
            name='test_installed_module',
            description='A test installed module',
            landing_url='/installed/'
        )
        response = self.client.get(reverse('module_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('all_modules', response.context)
        self.assertIn('installed_modules', response.context)
        installed_modules = response.context['installed_modules']
        self.assertIn('test_installed_module', list(installed_modules))

    def test_install_module_creates_installed_module_and_redirects(self):
        sample_app = apps.get_app_config('sample_module')
        response = self.client.get(reverse('install_module', args=['sample_module']))

        self.assertRedirects(response, sample_app.module_metadata['landing_url'])
        self.assertTrue(
            InstalledModule.objects.filter(name='sample_module').exists()
        )

    def test_uninstall_module_deletes_module_and_redirects(self):
        InstalledModule.objects.create(
            name='test_module',
            description='desc',
            landing_url='/test/'
        )
        response = self.client.get(reverse('uninstall_module', args=['test_module']))

        self.assertRedirects(response, '/module/')
        self.assertFalse(
            InstalledModule.objects.filter(name='test_module').exists()
        )

    def test_upgrade_module_migrations_and_redirect(self):
        sample_app = apps.get_app_config('sample_module')
        response = self.client.get(reverse('upgrade_module', args=['sample_module']))
        self.assertRedirects(response, sample_app.module_metadata['landing_url'])
