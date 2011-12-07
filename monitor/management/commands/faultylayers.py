#means to know layers and maps that are troublesome#means to know layers and maps that are troublesome#means to know layers and maps that are troublesome
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django.core.mail import mail_admins,
from django.conf import settings
from geonode.maps.models import Map, Layer
from monitor.models import FaultyLayer
import httplib
import urllib2,urllib
import simplejson
import os


def get_faulty_maps():
    """Gets a list of maps failing based on the FaultyLayer table.

       If a faulty layer is contained in a map it is marked as invalid.
       If two faulty layers are present in a map, this will return only one entry.
    """
    map_ids = []
    for layer in FaultyLayer.objects.all():
        map_ids.extend([themap.id for themap in layer.layer.maps()])
    # use the list of ids (possibly repeated) to filter out map objetcs.
    faulty_maps = Map.objects.filter(id__in=map_ids).distinct()
    return faulty_maps


def check_layers():
    """Tries to connect to the layer url and creates a FaultyLayer object if it can not do it.
    """
    url = urllib2.urlparse.urlsplit(settings.GEOSERVER_BASE_URL)[1]
    for layer in Layer.objects.all():
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = httplib.HTTPConnection(url,timeout=10)
        link = '/geoserver/wms/reflect?layers=' + layer.typename
        conn.request("GET",link,"",headers)
        r1 = conn.getresponse()
        status_code = r1.status
        contenttype = r1.getheader('Content-Type')
        reason = r1.read()
        perm = layer.get_all_level_info()
        if 'anonymous' not in  perm:
            reason = 'No permissions to query this'
        print '%s [%s]' % (link,status_code)

        # Only layers without an image content type are deemed to be irresponsible
        if contenttype != 'image/png':
            FaultyLayer.objects.create(layer=layer,error_code=status_code, reason=reason)
        conn.close()

    context = {} 
    context["name"] = settings.SITENAME
    context['url'] = settings.SITEURL
    context["geoserver_base_url"] = settings.GEOSERVER_BASE_URL
    context["geonetwork_base_url"] = settings.GEONETWORK_BASE_URL
    context["layer_count"] =  Layer.objects.count()
    context["map_count"] = Map.objects.count()
    context["faulty_layers"] = FaultyLayer.objects.all()
    context["faulty_maps"] = get_faulty_maps()
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
