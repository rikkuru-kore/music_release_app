from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Items)
admin.site.register(models.Orders)
admin.site.register(models.Inquiry)