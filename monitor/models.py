from django.db import models
from geonode.maps.models import Layer


class FaultyLayer(models.Model):
    layer = models.ForeignKey(Layer)
    error_code = models.IntegerField()
    check_date = models.DateTimeField(auto_now_add=True, help_text="Date the layer was known to have problems.")
    reason = models.TextField(null=True, blank=True, help_text="Longer description about the error, if possible with a traceback.")

    def affected_maps(self):
        """Returns the maps affected for this layer being problematic.
        """
        self.layer.maps()

    def __unicode__(self):
        return self.layer.name
