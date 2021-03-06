# coding=utf-8

from __future__ import unicode_literals

from django.http import Http404
from django.test.client import RequestFactory
from django_app.mongo_test_case import MongoTestCase
from mock import patch

from django_short_urls.views import main
from django_short_urls.models import Link


class ViewMainTestCase(MongoTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.path = 'test42'
        self.link = Link.shorten('http://www.work4.com/jobs', short_path=self.path)

    @patch('django_short_urls.views.statsd')
    def test_redirect(self, mock_statsd):
        self.assertEqual(
            main(self.factory.get('/%s' % self.path), self.path).status_code,
            302
        )
        self.assertEqual(self.link.reload().clicks, 1)
        mock_statsd.increment.assert_called_once()

    def test_redirect_suffix(self):
        response = main(self.factory.get('/%s/recruiter' % self.path), self.path + '/recruiter')

        self.assertEqual(response.status_code, 302)

    def test_404(self):
        path404 = self.path + 'foobar'

        with self.assertRaises(Http404):
            main(self.factory.get('/%s' % path404), path404)

        with self.assertRaises(Http404):
            main(self.factory.get('/%s/' % path404), path404 + '/')
