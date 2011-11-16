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

     	     
