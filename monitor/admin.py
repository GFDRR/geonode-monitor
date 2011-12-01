from monitor.models import FaultyLayer
from django.contrib import admin

class FaultyLayerAdmin(admin.ModelAdmin):
    list_display = ['layer_name', 'error_code']

admin.site.register(FaultyLayer, FaultyLayerAdmin)


