#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Define the endpoints entries for the application."""

import endpoints

from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext.ndb import GeoPt
from google.appengine.ext import ndb
from model.photo_model import PhotoModel



package = 'instafetcher.api'


class Photo(messages.Message):
    """Represent the model for a single image in the endpoints data."""
    id = messages.StringField(1)
    url = messages.StringField(2)
    lon = messages.FloatField(3)
    lat = messages.FloatField(4)


class PhotoCollection(messages.Message):
    """Represent the model for a single image in the endpoints data."""
    items = messages.MessageField(Photo, 1, repeated=True)


class GeoPoint(messages.Message):
    """Represent the model for a coordinate point in the endpoints data"""
    lat = messages.FloatField(1)
    lon = messages.FloatField(2)


class GeoPointCollection(messages.Message):
    """Represent the model for a GeoPoint collection in the endpoints data"""
    items = messages.MessageField(GeoPoint, 1, repeated=True)


@endpoints.api(name='instafetcher', version='v1')
class InstaFetcherApi(remote.Service):
    """InstaFetcher API v1.

    Defines the Endpoints methods and logic for
    the application API.
    """

    PAGE_RESOURCE = endpoints.ResourceContainer(
        message_types.VoidMessage,
        page=messages.IntegerField(1, variant=messages.Variant.INT32)
    )

    @endpoints.method(PAGE_RESOURCE, PhotoCollection,
                      path='images/{page}', http_method='GET',
                      name='img.listImages')
    def image_list(self, request):
        """Gets the photo collection at the given page in the Datastore.

        Parameters:
            request: Contains information of the user request call

        Returns:
            The photo collection at the given page in the Datastore.
        """
        query = ("SELECT * FROM PhotoModel " +
                 "ORDER BY date_stored " +
                 "LIMIT {l1}, 20".format(l1=request.page * 20))
        data = ndb.gql(query)
        images = list()
        for img in data.fetch():
            images.append(Photo(id=img.photo_id, url=img.url,
                                lon=img.longitude, lat=img.latitude))
        return PhotoCollection(items=images)

    @endpoints.method(message_types.VoidMessage, GeoPointCollection,
                      path='coordinates/', http_method='GET',
                      name='img.listCoordinates')
    def coordinate_list(self, unused_request):
        """Gets the coordinates of the last x photos in the Datastore.

        Returns:
            The latest coordinates in the Dastore.
        """
        query = ("SELECT latitude, longitude FROM PhotoModel " +
                 "ORDER BY date_stored")
        data = ndb.gql(query)
        coordinates = list()
        for coordinate in data.fetch():
            coordinates.append(GeoPoint(lat=coordinate.latitude,
                                        lon=coordinate.longitude))
        return GeoPointCollection(items=coordinates)

APPLICATION = endpoints.api_server([InstaFetcherApi])