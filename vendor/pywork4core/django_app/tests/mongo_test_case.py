# coding=utf-8

from __future__ import unicode_literals

from mongoengine import Document

from django_app import mongo_test_case


class MongoTestCaseTestCase(mongo_test_case.MongoTestCase):
    class MongoDoc(Document):
        pass

    def test(self):
        self.database.test_collection.insert({'foo': 'bar'})

        self.MongoDoc().save()
