# coding=utf-8

"""
WSGI config for django_short_urls project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
from __future__ import unicode_literals

import os
import site


# pylint: disable=W0511
# FIXME: Use PyUnicorn+Foreman...
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
site.addsitedir(os.path.join(ROOT_DIR, 'venv/lib/python2.7/site-packages'))
site.addsitedir(ROOT_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_short_urls.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
# pylint: disable=C0103
application = get_wsgi_application()
