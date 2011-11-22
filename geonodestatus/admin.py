from geonode.maps.models import Map, Layer, MapLayer, Contact, ContactRole, Role
from geonode.geonodestate.models import Badlayers,BadMaps
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class MapLayerInline(admin.TabularInline):
	model = BadMaps
	
class LayerAdmin(admin.ModelAdmin):
	inlines = [MapLayerInline]

admin.site.register(Badlayers)

