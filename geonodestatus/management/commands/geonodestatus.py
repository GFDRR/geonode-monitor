#means to know layers and maps that are troublesome#means to know layers and maps that are troublesome#means to know layers and maps that are troublesome
from django.core.management.base import BaseCommand,CommandError
from geonode.maps.models import Map, Layer, MapLayer
from geonode.geonodestate.models import Badlayers,BadMaps
from django.shortcuts import render_to_response, get_object_or_404
import urllib2
from datetime import datetime
import simplejson
from django.conf import settings


class Command(BaseCommand):
	help = 'Report maps and layers that are troublesome and log them'
	args = '[none]'
	def handle(self, *args, **keywordargs):
		host = settings.SITEURL
		layerapi = host + 'data/search/api'
		#we first check out the layers and log them
		def get_url(url):
			try:
				'''returns the response of any url'''
				request = urllib2.Request(url)
				opener = urllib2.build_opener()
				f = opener.open(request)
				#print '%s [%s]' % (url,f.getcode())
				return f
			except urllib2.HTTPError, e:
				print '%s [%s]' % (url,e.code)
				errorcode = e.code
				#we now get maps if this layer has any
				layermaps = check_map(url)
				layer=returnlayer(url)
                                if len(layermaps) > 0:
                                   #we now store layes with no maps attached
                                   #storebadlayer(layer=returnlayer(url))
       
                                   for i in layermaps:
                                   	   failmap = Map.objects.get(pk=i)
                                   	   Badlayers.objects.create(layername=layer.name,errorcode=errorcode,content_object=failmap)
                                else:
                                   #we now deal with layers with no maps attached
                                   storebadlayer(layer,errorcode)
                           	   
                                   
                def returnlayer(url):
                  #method that returns a layer
                  layername = url.split('/')
                  layername = layername[4]
                  layer = get_object_or_404(Layer,typename=layername)
                  return layer
                def storebadlayer(layer,code):
                	#we store to the database
                	#print layer.name
                	#badlayer = Badlayers(layername=layer.name,errorcode=code)
                	faillayer = Badlayers.objects.create(layername=layer.name,errorcode=code)
                	#badlayer.save(force_insert=True)
                	return faillayer
                	
                def check_map(url):
                	#pass the layer url to get the map affected
			layername = url.split('/')
			layername = layername[4]
			#layer = get_object_or_404(Layer, typename=layername)
                        maplayer = MapLayer.objects.filter(name=layername)
                        maps =  []
                        for map in maplayer:
                            #print  map.map.id
                            maps.append(map.map.id)
                        return maps
                            
		#we do the check on the layers/data api
		def inspect_layers(data):
			layers = data['rows']
			for detail in layers:
				layer_url = detail['detail']
				layer_name = detail['name']
				get_url(layer_url)
		try:
			print "checking layers"
			while(True):
				f = get_url(layerapi)
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
			print "could not connect to GeoServer. Pole"
						
					
