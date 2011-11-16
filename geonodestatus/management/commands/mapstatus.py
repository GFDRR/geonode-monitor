from django.core.management.base import BaseCommand,CommandError
from django.conf import settings
import urllib2
from utils import *
import simplejson
from geonode.maps.models import Map,MapLayer
from django.shortcuts import render_to_response, get_object_or_404

class Command(BaseCommand):
   help = 'Report maps that have unavailable layers'
   args = '[none]'
   def handle(self, *args, **keywordargs):
      host = settings.SITEURL
      url = host + 'maps/search/api'
      def get_layers(mapurl):
          #this method gets all the layers belonging to a mapi
          print 'checking the map %s' % mapurl
          mapid =  mapurl.split('/')
          mapid= mapid[2]
          map = get_object_or_404(Map,pk=mapid)          
          layers = MapLayer.objects.filter(map=map.id)
          for layer in layers:
              if layer.group != 'background':
                  #we get the layer url page
                  layer_url = host + 'data/' + layer.name
                  #we pass each layer to the method to check for its availability
                  ping_layers(layer_url)
              else:
                  continue
      def inspect_maps(data):
          maps = data['rows']
          for detail in maps:
              mapurl = detail['detail']
              #we now pass each and every map to get all the layers in that map
              get_layers(mapurl)  
      try:
         print "checking maps"
         while(True):
             f = get_url(url)
             data = simplejson.load(f)
             inspect_maps(data)
             if len(data['rows']) > 0:
                try:
                    url = host + data['next']
                    continue
                except KeyError:
                    #print "Error on the key"
                    break
             else:
                break
      except CommandError,e:
         print e

