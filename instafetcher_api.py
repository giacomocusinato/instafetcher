import endpoints

from protorpc import messages
from protorpc import message_types
from protorpc import remote
from google.appengine.ext import db
from main import InstaImage

# TODO: Replace the following lines with client IDs obtained from the APIs
# Console or Cloud Console.
WEB_CLIENT_ID = 'replace this with your web client application ID'
ANDROID_CLIENT_ID = 'replace this with your Android client ID'
IOS_CLIENT_ID = 'replace this with your iOS client ID'
ANDROID_AUDIENCE = WEB_CLIENT_ID


package = 'InstaFetcherApi'


class Image(messages.Message):
    """A single image"""
    id = messages.StringField(1)
    url = messages.StringField(2)


class ImageCollection(messages.Message):
    """A image list"""
    items = messages.MessageField(Image, 1, repeated=True)


@endpoints.api(name='instafetcher', version='v1',
               allowed_client_ids=[WEB_CLIENT_ID, ANDROID_CLIENT_ID,
                                   IOS_CLIENT_ID],
               audiences=[ANDROID_AUDIENCE])
class InstaFetcherApi(remote.Service):
    """InstaFetcher API v1"""

    @endpoints.method(message_types.VoidMessage, ImageCollection,
                      path='images', http_method='GET',
                      name='img.listImages')
    def image_list(self, unused_request):
        data = db.GqlQuery("SELECT * FROM InstaImage")
        images = list()
        for img in data.run(limit=20):
            images.append(Image(id=img.photo_id, url=img.url))
        return ImageCollection(items=images)

APPLICATION = endpoints.api_server([InstaFetcherApi])