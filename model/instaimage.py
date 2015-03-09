#!/usr/bin/env python
# -*- coding: utf-8 -*-

from google.appengine.ext import db

package = 'instafetcher.model'


class PhotoModel(db.Model):
    """Model representing an Instagram photo object
     to be stored in the Google Cloud Datastore.

     Attributes:
        photo_id: unique identifier of the object.
        url: url of the photo.
        date_stored: the date on witch the photo was saved.
    """
    photo_id = db.StringProperty(indexed=True)
    url = db.StringProperty(indexed=False)
    date_stored = db.StringProperty(indexed=False)