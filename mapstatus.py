from django.core.management.base import BaseCommand,CommandError
from django.conf import settings
import urllib2
import simplejson

class Command(BaseCommand):
   help = 'Report maps that have unavailable layers'
   args = '[none]'
   def handle(self, *args, **keywordargs):
      host = settings.SITEURL
      url = host + 'maps/search/api'
      #method to query that maps api
      def get_url(url):
        try:
           '''Returns the response object of the maps api url'''
           request = urllib2.Request(url)
           opener = urllib2.build_opener()
           f = opener.open(request)
           return f
        except urllib2.HTTPError:
            print "No maps available"
      try:
         print "checking maps"
         while(True):
             f = get_url(url)
             data = simplejson.load(f)
             #inspect_maps(data)
             if len(data['rows']) > 0:
                try:
                    url = host + data['next']
                    continue
                except KeyError:
                    print "Error on the key"
                    break
             else:
                break
      except CommandError,e:
         print e
