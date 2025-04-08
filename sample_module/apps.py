from django.apps import AppConfig
from django.db.models.signals import post_migrate


class SampleModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sample_module'

    module_metadata = {
        'name': 'Sample Module',
        'description': 'Sample Product.',
        'landing_url': '/products/',
    }

    def ready(self):
        post_migrate.connect(self.setup_roles_and_demo_data, sender=self)
    
    def setup_roles_and_demo_data(self, **kwargs):
        from django.contrib.auth.models import Group, Permission
        from django.contrib.contenttypes.models import ContentType
        Product = self.get_model('Product')

        content_type = ContentType.objects.get_for_model(Product)

        # Auto-create groups and permissions if not exists
        for role, perms in {
            'manager': ['add_product', 'change_product', 'delete_product', 'view_product'],
            'user': ['add_product', 'change_product', 'view_product'],
            'public': ['view_product']
        }.items():
            group, _ = Group.objects.get_or_create(name=role)
            for perm_code in perms:
                perm = Permission.objects.get(codename=perm_code, content_type=content_type)
                group.permissions.add(perm)
