from django.contrib import admin
from .models import InstalledModule

@admin.register(InstalledModule)
class InstalledModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'landing_url', 'installed_at')
    search_fields = ('name',)
