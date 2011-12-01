from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class FaultyLayer(models.Model):
    layer_name = models.CharField(max_length=128)
    error_code = models.CharField(max_length=25)
    created = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType,null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = generic.GenericForeignKey()

    def __unicode__(self):
        return self.layername
