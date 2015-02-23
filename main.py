#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import json
import urllib2

from google.appengine.ext import db


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')


class InstaImage(db.Model):
    photo_id = db.StringProperty(indexed=True)
    url = db.StringProperty(indexed=False)


class CronHandler(webapp2.RequestHandler):
    def get(self):
        req_url = ("https://api.instagram.com/v1/tags/nban/media/recent?"
                   "client_id=8e2555402533429aa5c5c193334a988b")
        data = json.load(urllib2.urlopen(req_url))

        img_list = data["data"]
        for img in img_list:
            # stored = CronHandler.already_stored(img["id"])
            image = InstaImage()
            image.photo_id = img["id"]
            image.url = img["images"]["standard_resolution"]["url"]
            image.put()

    @staticmethod
    def already_stored(img_id):
        print img_id
        data = InstaImage.all()
        data.filter("photo_id =", img_id)

        if data.get() is not None:
            return False
        else:
            return True


app = webapp2.WSGIApplication([
    ('/cron/fetch', CronHandler)
], debug=True)