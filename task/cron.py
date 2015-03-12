#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Define the CronHandler class.
"""

import webapp2
import json
import urllib2
import datetime
import logging

from model.instaimage import PhotoModel
from google.appengine.ext.ndb import GeoPt
from google.appengine.ext import ndb

package = "instafetcher.task"


class CronHandler(webapp2.RequestHandler):
    """Define the logic to be executed in the cron task."""

    @staticmethod
    def get():
        """Uses the Instagram API to fetch the #nban photo feed
        and store every image data in the datastore.
        """
        # Instagram API request URL
        req_url = ("https://api.instagram.com/v1/tags/nban/media/recent?"
                   "client_id=8e2555402533429aa5c5c193334a988b")
        data = json.load(urllib2.urlopen(req_url))

        photo_list = data["data"]
        for img in photo_list:
            if CronHandler.already_stored(img["id"]):
                pass
            else:
                photo = PhotoModel()
                photo.photo_id = img["id"]
                photo.url = img["images"]["standard_resolution"]["url"]
                photo.date_stored = datetime.datetime.now().isoformat()

                if img["location"] is not None:
                    photo.longitude = img["location"]["latitude"]
                    photo.latitude = img["location"]["longitude"]

                photo.put()

    @staticmethod
    def already_stored(photo_id):
        """Check if the photo is already stored in the Datastore.

        Parameters:
            photo_id: the photo_id relative to the PhotoModel
            stored in the Datastore.

        Returns:
            A boolean value of True if the PhotoModel with the given
            photo_id is stored in the Datastore, False otherwise.
        """
        logging.info("Starting already_stored method")

        data = ndb.gql("SELECT * FROM PhotoModel " +
                       "WHERE photo_id='{id}'".format(id=photo_id))

        logging.info(data.fetch())

        if data.fetch() == []:
            return False
        else:
            return True


app = webapp2.WSGIApplication([
    ('/cron/fetch', CronHandler)
], debug=True)
