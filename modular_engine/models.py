from django.db import models

class InstalledModule(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    landing_url = models.CharField(max_length=100)
    installed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
