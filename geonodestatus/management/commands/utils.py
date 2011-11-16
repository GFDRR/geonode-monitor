import urllib2
def get_url(url):
   try:
     '''Returns the response object of the maps api url'''
     request = urllib2.Request(url)
     opener = urllib2.build_opener()
     f = opener.open(request)
     return f
   except urllib2.HTTPError, e:
     print e
def ping_layers(layer_url):
   try:
      f = get_url(layer_url)
      try:
          code = f.getcode()
      except:
          return False
      print '%s [%s]' % (layer_url, code)
   except urllib2.HTTPError, e:
      print '%s [%s]' % (layer_url,code)

