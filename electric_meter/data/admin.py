from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Purchase

admin.site.register(Purchase)

