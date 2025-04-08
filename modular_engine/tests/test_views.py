from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from modular_engine.models import InstalledModule


class ModularEngineViewTests(TestCase):
    def setUp(self):
        InstalledModule.objects.create(
            name='installed_module',
            description='An installed module',
            landing_url='/installed/'
        )

    @patch('modular_engine.views.apps.get_app_configs')
    def test_module_list_view(self, mock_get_app_configs):
        mock_app_config = MagicMock()
        mock_app_config.module_metadata = {'description': 'desc', 'landing_url': '/products/'}
        mock_app_config.name = 'sample_module'
        mock_get_app_configs.return_value = [mock_app_config]

        response = self.client.get(reverse('module_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('all_modules', response.context)
        self.assertIn('installed_modules', response.context)

    @patch('modular_engine.views.call_command')
    @patch('modular_engine.views.apps.get_app_config')
    def test_install_module(self, mock_get_app_config, mock_call_command):
        mock_app_config = MagicMock()
        mock_app_config.name = 'sample_module'
        mock_app_config.label = 'sample_module'
        mock_app_config.module_metadata = {
            'description': 'Sample description',
            'landing_url': '/products/'
        }
        mock_get_app_config.return_value = mock_app_config

        response = self.client.get(reverse('install_module', args=['sample_module']))
        self.assertRedirects(response, '/products/')
        self.assertTrue(InstalledModule.objects.filter(name='sample_module').exists())
        mock_call_command.assert_any_call('makemigrations', 'sample_module')
        mock_call_command.assert_any_call('migrate', 'sample_module')

    def test_uninstall_module(self):
        InstalledModule.objects.create(name='test_module', description='desc', landing_url='/test/')
        response = self.client.get(reverse('uninstall_module', args=['test_module']))
        self.assertRedirects(response, '/module/')
        self.assertFalse(InstalledModule.objects.filter(name='test_module').exists())

    @patch('modular_engine.views.call_command')
    @patch('modular_engine.views.apps.get_app_config')
    def test_upgrade_module(self, mock_get_app_config, mock_call_command):
        mock_app_config = MagicMock()
        mock_app_config.name = 'sample_module'
        mock_app_config.label = 'sample_module'
        mock_app_config.module_metadata = {
            'description': 'Sample description',
            'landing_url': '/products/'
        }
        mock_get_app_config.return_value = mock_app_config

        response = self.client.get(reverse('upgrade_module', args=['sample_module']))
        self.assertRedirects(response, '/products/')
        mock_call_command.assert_any_call('makemigrations', 'sample_module')
        mock_call_command.assert_any_call('migrate', 'sample_module')
