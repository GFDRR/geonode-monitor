from django.core.management.base import BaseCommand,CommandError
import urllib2
from utils import *
import simplejson
from django.conf import settings

from geonode.maps.models import Map, Layer
from django.shortcuts import render_to_response, get_object_or_404

class Command(BaseCommand):
    help = 'Report trouble some layers'
    args = '[none]'
    def handle(self, *args, **keywordargs):
        host = settings.SITEURL
        url  = host + 'data/search/api'
        def totallayers(data):
            total = data['total']
            return total
        def check_map(layer):
            #we check if the layer is in any map if true return the maps
            layer = get_object_or_404(Layer, typename=layer)
            print 'this layer affects the following maps'
            for map in layer.maps():
            	    print 'this layer affects the following maps'
        def inspect_layers(data):
            """Iterates over a list of layers printing the result
            """
            #after the fetch we get the layers
            layers = data['rows']
            #get the datasets directory from the search api
            #we traverse each and evey layer to get out detailpage
            for detail in layers:
                layer_url = detail['detail']
                layer_name = detail['name']
                #we get the code, if the data is available/clean then we return the stream else the code
                code = get_url(layer_url)
                check_map(layer_name)
                
                '''if (code == 401):
                        #we now check if it is in any map
                        check_map(layer_name)
                elif(code == 500):
                	#we check for it being in any map
                	check_map(layer_name)
                else:
                	continue'''
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
            
