from monitor.models import FaultyLayer
from django.contrib import admin

class FaultyLayerAdmin(admin.ModelAdmin):
    list_display = ['layer', 'error_code']

admin.site.register(FaultyLayer, FaultyLayerAdmin)


