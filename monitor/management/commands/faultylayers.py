#means to know layers and maps that are troublesome#means to know layers and maps that are troublesome#means to know layers and maps that are troublesome
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import mail_admins
from django.conf import settings
from django.utils import simplejson
from geonode.maps.models import Map, Layer
from monitor.models import FaultyLayer
from xml.dom.minidom import parseString
import httplib
import urllib2
import datetime
import os


def get_faulty_maps(check_date):
    """Gets a list of maps failing based on the FaultyLayer table.

       If a faulty layer is contained in a map it is marked as invalid.
       If two faulty layers are present in a map, this will return only one entry.
    """
    map_ids = []
    for layer in FaultyLayer.objects.filter(check_date=check_date):
        map_ids.extend([themap.id for themap in layer.layer.maps()])
    # use the list of ids (possibly repeated) to filter out map objetcs.
    faulty_maps = Map.objects.filter(id__in=map_ids).distinct()
    return faulty_maps
    
    
def get_url(host, path, headers={}):
    """Gets the content or status code of a url.
       If there is an error connecting, it returns -1 as the status code.
        
       Output: Dictionary with status code, response and reason.
    """
    conn = httplib.HTTPConnection(host,timeout=10)
    conn.request("GET",path, None,headers)
    try:
       response = conn.getresponse()
       status_code = response.status
       contenttype = response.getheader('Content-Type')
       reason = response.read()
       conn.close()
       return status_code, contenttype, reason
    except Exception, e:
       return -1, None, str(e)
def check_layers():
    """Tries to connect to the layer url and creates a FaultyLayer object if it can not do it.
    """
    url = urllib2.urlparse.urlsplit(settings.GEOSERVER_BASE_URL)[1]
    geonodeurl = urllib2.urlparse.urlsplit(settings.SITEURL)[1]
    check_date = datetime.datetime.now()
    for layer in Layer.objects.all():
        detail_code, detail_contenttype, detail_reason = get_url(geonodeurl,
                                                                 layer.get_absolute_url())
        # Check if the detail page works (401 is excluded too)
        detail_page_fails  = detail_code not in [200, 401]

        # Check for pink layers.
        perm = layer.get_all_level_info()
        if 'anonymous' in  perm:
            headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
            wmslink = '/geoserver/wms/reflect?layers=' + layer.typename
            wms_code, wms_contenttype, wms_reason = get_url(url, wmslink, headers)
            pink_tile = wms_contenttype != 'image/png'
        
        else:
            # Avoid checking the protected ones for pink tiles.
            pink_tile = False

        if detail_page_fails:
            #FIXME: Extract title from XML if possible, if not, store the whole document.
            title = None
            #dom = parseString(detail_reason)
            #title = dom.getElementsByTagName("title")[0]
            if title is not None:
                reason = title
            else:
                reason = detail_reason
        elif pink_tile:
            reason = 'The layer is not rendering: %s' % wms_reason

        # Only layers without an image content type are deemed to be irresponsible
        if pink_tile or detail_page_fails:
            print '%s (failed) http://%s%s' % (layer.name,
                                   geonodeurl, layer.get_absolute_url())
            FaultyLayer.objects.create(layer=layer,error_code=detail_code,
                                       reason=reason, check_date=check_date)
            
        else:
            print '%s (ok)'  % layer.name

    faulty_layers =  FaultyLayer.objects.filter(check_date=check_date)

    my_dict = {}
    for layer in faulty_layers:
        my_dict.setdefault(layer.layer.typename,[]).append(layer.layer.typename)
        my_dict.setdefault(layer.layer.typename, []).append(layer.layer.get_absolute_url()) 
        my_dict.setdefault(layer.layer.typename, []).append(layer.reason) 

    #print my_dict
    context = {}
    context["name"] = settings.SITENAME
    context['url'] = settings.SITEURL
    context["geoserver_base_url"] = settings.GEOSERVER_BASE_URL
    context["geonetwork_base_url"] = settings.GEONETWORK_BASE_URL
    context["layer_count"] =  Layer.objects.count()
    context["map_count"] = Map.objects.count()
    context["faulty_layers"] = FaultyLayer.objects.filter(check_date=check_date)
    context["faulty_layers_status"] = my_dict
    context["faulty_maps"] = get_faulty_maps(check_date)
    context["backup_date"] = backupdate()
    return context

def send_admin_email(context):
    """This is the function that sends the site administrators an email on faulty layer and faulty maps"""
    # Do not send email of that setting is not defined.
    if len(context["faulty_layers"]) == 0:
        return
    subject = 'Problematic layers at %s' % settings.SITENAME
    message = render_to_string('../templates/admin_email.txt', context)
    mail_admins(subject, message, fail_silently=False)


def backupdate():
    """this function returns the date of the last backup
    """
    #we start with directory of the backups
    filename = settings.GEONODE_BACKUP_DIR
    try:
        t = os.path.getmtime(filename)
    #FIXME: Change the filename to an invalid one and pin down the exception type.
    except:
        t = None
    return t

def send_registry(context):
    """This function deals pushing logs/data to the geonode registry
    """
    # Do not send email of that setting is not defined.
    #FIXME: Put this as a warning in the logs.
    if settings.GEONODE_REGISTRY_URL is None:
        return

    #we get the registry url
    registry_site = settings.GEONODE_REGISTRY_URL
    # Send only the count to avoid serialization problems.
    context["faulty_layers_count"] = context["faulty_layers"].count()
    context["faulty_maps_count"] = context["faulty_maps"].count()
    context.__delitem__('faulty_layers')
    context.__delitem__('faulty_maps')

    regdump = simplejson.dumps(context)
    data = regdump.encode('utf-8')
    #we now perform the post
    postlink = registry_site + 'registry/geonode/'
    print 'Sending request to', postlink
    req = urllib2.Request(postlink, data)
    response = urllib2.urlopen(req)

class Command(BaseCommand):
    help = 'Report maps and layers that are troublesome and log them'
    args = '[none]'

    def handle(self, *args, **keywordargs):
        context = check_layers()
        send_admin_email(context)
        send_registry(context)
