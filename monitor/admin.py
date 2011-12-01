from monitor.models import Badlayers,BadMaps
from django.contrib import admin

class MapLayerInline(admin.TabularInline):
    model = BadMaps
    list_display = ['layer', 'error_code']

class LayerAdmin(admin.ModelAdmin):
    inlines = [MapLayerInline]

admin.site.register(Badlayers)

