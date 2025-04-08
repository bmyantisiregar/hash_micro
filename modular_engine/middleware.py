from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
from .models import InstalledModule

class ModuleLandingPageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # If user is not authenticated, let auth handle it
        if not request.user.is_authenticated:
            return None

        path = request.path.strip('/')
        installed_modules = InstalledModule.objects.values_list('landing_url', flat=True)
        
        if f'/{path}/' in installed_modules:
            return None
        
        if path.startswith('products') and not installed_modules:
            return redirect('/module/')


        return None
