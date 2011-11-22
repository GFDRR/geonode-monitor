from django.db import models
from datetime import datetime
from geonode.maps.models import Map, Layer, MapLayer
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Badlayers(models.Model):
    layername = models.CharField("Layer",max_length=128)
    errorcode = models.CharField("Error Code",max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType,null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey()
    #content_type = models.ForeignKey(ContentType)
    def __unicode__(self):
    	    return self.layername
    class Meta:
    	    verbose_name_plural ='Faulty Layers'
#links to maps that are troublesome
class BadMaps(models.Model):
     #title = models.CharField(max_length=128)
     errormap = models.ForeignKey(Map)
     layer = models.ForeignKey(Badlayers)
     def __unicode__(self):
     	     return self.errormap.title
     class Meta:
     	     verbose_name_plural = "Faulty Maps"
     	     verbose_name = "Maps"

