from django.apps import apps
from django.contrib import admin

# Register your models here.

for model in apps.get_app_config('littlebytes').models.values():
    admin.site.register(model)
