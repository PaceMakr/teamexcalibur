from django.contrib import admin

# Register your models here.
from .models import Inventory, Log

admin.site.register(Inventory)
admin.site.register(Log)

