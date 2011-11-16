from django.core.management.base import BaseCommand,CommandError
import urllib2
import simplejson
from utils import *
from django.conf import settings

class Command(BaseCommand):
    help = 'Report trouble some layers'
    args = '[none]'
    def handle(self, *args, **keywordargs):
        host = settings.SITEURL
        #host = 'http://horn.rcmrd.org/'
 
        url  = host + 'data/search/api'
        def totallayers(data):
            total = data['total']
            return total
        def inspect_layers(data):
            """Iterates over a list of layers printing the result
            """
            #after the fetch we get the layers
            layers = data['rows']
            #get the datasets directory from the search api
            #we traverse each and evey layer to get out detailpage
            for detail in layers:
                layer_url = detail['detail']
                ping_layers(layer_url)
        try:
            print "checking layers"
            while(True):
                f = get_url(url)
                data = simplejson.load(f)
                inspect_layers(data)
                if len(data['rows']) > 0:
                   try:
                       url = host + data['next'] 
                       continue
                   except KeyError:
                       break
                else:
                   break
        except CommandError,e:
            print "Couldn't connect to GeoServer; is it running? Make sure the GEOSERVER_BASE_URL setting is set correctly."
