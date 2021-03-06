# coding=utf-8

from __future__ import unicode_literals

from django.test import TestCase

from django_short_urls.int_to_alnum import ALPHABET, encode, decode


# pylint: disable=E1101
class IntToAlnumTestCase(TestCase):
    def test(self):
        value = 123456789

        self.assertEquals(decode(encode(value)), value)

        self.assertEquals(encode(0), ALPHABET[0])
