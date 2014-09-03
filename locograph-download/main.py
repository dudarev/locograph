import sys
sys.path[0:0] = ['lib']

import logging
import os
import cloudstorage as gcs
import webapp2

from google.appengine.api import app_identity

FILE_URL_TEMPLATE = "http://storage.googleapis.com/{bucket_name}/{object_name}"


my_default_retry_params = gcs.RetryParams(initial_delay=0.2,
                                          max_delay=5.0,
                                          backoff_factor=2,
                                          max_retry_period=15)
gcs.set_default_retry_params(my_default_retry_params)
bucket_name = os.environ.get('BUCKET_NAME',
                             app_identity.get_default_gcs_bucket_name())
BUCKET = '/' + bucket_name


class MainPage(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        self.response.write('This is app for downloading places extracts.')


class DownloadPage(webapp2.RequestHandler):
    def get(self, *args, **kwargs):
        bucket_name = os.environ.get('BUCKET_NAME',
                                     app_identity.get_default_gcs_bucket_name())
        bucket = '/' + bucket_name
        # omit first '/'
        object_name = self.request.path[1:]
        try:
            stat = gcs.stat(bucket + '/' + object_name)
            logging.info(repr(stat))
        except gcs.errors.NotFoundError:
            self.abort(404)
        except gcs.errors.AuthorizationError:
            self.abort(404)
        except Exception, e:
          logging.exception(e)
          self.response.write('There was an error: {}'.format(e))
        self.redirect(FILE_URL_TEMPLATE.format(
            bucket_name=bucket_name, object_name=object_name))


app = webapp2.WSGIApplication([
    (r'/', MainPage),
    (r'/(.*)', DownloadPage)
    ], debug=True)
