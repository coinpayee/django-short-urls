# coding=utf-8

"""Module to manipulate requests, HTML and HTTP concepts"""

from __future__ import unicode_literals

from django.http import HttpResponse, QueryDict
import json
import requests
from urllib import urlencode
import urlparse

from http.status import HTTP_OK


def validate_url(url):
    """Validates that a url has a valid structure"""

    parsed_url = urlparse.urlparse(url)

    if not parsed_url.netloc:
        return (False, "Url structure is invalid: '%s'" % url)

    if parsed_url.scheme not in ('http', 'https'):
        return (False, "Unsupported URL scheme: '%s'" % url)

    if parsed_url.password:
        return (False, "URLs containing passwords are not supported: '%s'" % url)

    return (True, None)


def url_append_parameters(url, params_to_replace, defaults):
    '''
    Appends the REDIRECT_PARAM_NAME param and the shorten's GET params
    to the long URL.
    Takes QueryDicts as parameters
    '''

    if not params_to_replace and not defaults:
        return url

    # pylint: disable=W0633
    (scheme, netloc, path, params, link_query, fragment) = urlparse.urlparse(url)

    link_query = QueryDict(link_query).copy()

    for key, value in params_to_replace.iteritems():
        link_query[key] = value

    for key, value in defaults.iteritems():
        if key not in link_query:
            link_query[key] = value

    return urlparse.urlunparse((
        scheme, netloc, path, params,
        urlencode(link_query),
        fragment
    ))


def response(message=None, status=HTTP_OK, **kwargs):
    """Builds a json response with the kwargs object and some additional standardized fields"""
    kwargs.update({
        "status_code": status,
        "error": status != HTTP_OK,
        "message": message
    })

    return HttpResponse(json.dumps(kwargs), status=status, mimetype="application/json")


def proxy(url):
    """Loads url and returns its contents as a proxied web page"""
    resp = requests.get(url)

    return HttpResponse(
        resp.content,
        status=resp.status_code,
        mimetype=resp.headers['Content-Type'])
