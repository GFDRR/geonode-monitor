The purpose of the GeoNode Monitor is to provide admins of a GeoNode instance with reports on a GeoNode Instance they administer.

This is a simple django app embedded into the GeoNode base whose main purpose would be to log most of the events that occur within the GeoNode. This events for now will be limited to basic kinds of status requests. This will provide users with the following information on their GeoNode.

           * Status on Broken Pages
           * Status on Broken Maps
           * Mail the admin on pages and maps that are broken
           * Check for Broken server and broken geonetwork
           * Return number of broken layers and maps

This script is a simple django app that checks for pink layers.It logs the pink layers into a database. This data is then pushed to the geonode registry.

There is a bug with protected layers. Since we can not do a wms extend request to them without an active geoserver session,the reason is stored as being unavailable.

This means most unprotected layers will be shown as being faulty. Installing all one needs to do is to add the application to the settings file. One also needs to change the settings file back up directory, please ensure This is the location where you regularly perform your backups

#. Make sure the virtualenv is activated
#. Install from this repo using pip::

    pip install -e git+git://github.com/GFDRR/geonode-monitor.git#egg=monitor

#. Add this app to the ``INSTALLED_APPS`` setting in ``local_settings.py``::

     INSTALLED_APPS = (
                       ...
                       'monitor',
                       ....
                      )

#. Run it with the ``geonode`` binary or the ``django-admin.py`` executable::

     geonode faultylayers

   or::

     django-admin.py faultylayers --settings=geonode.settings

Added a set up file to make installation easier and add it into the django installed apps.
