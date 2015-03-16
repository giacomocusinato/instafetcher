#!/usr/bin/env python
# -*- coding: utf-8 -*-


from google.appengine.ext import ndb


package = 'instafetcher.model'


class PhotoModel(ndb.Model):
    """Model representing an Instagram photo object
     to be stored in the Google Cloud Datastore.

     Attributes:
        photo_id: unique identifier of the object.
        url: url of the photo.
        date_stored: the date on witch the photo was saved.
    """
    photo_id = ndb.StringProperty(indexed=True)
    url = ndb.StringProperty(indexed=False)
    date_stored = ndb.StringProperty(indexed=True)
    latitude = ndb.FloatProperty(indexed=True)
    longitude = ndb.FloatProperty(indexed=True)