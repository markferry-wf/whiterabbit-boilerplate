__author__ = 'Richie Foreman <richie.foreman@gmail.com>'
import settings
import app
from google.appengine.api import backends
import logging

@app.wsgi.route("/backends/test")
class BackendHandler(app.BaseHandler):
    def post(self):
        logging.info(str(backends.get_backend()) + "I'm a backend..")
        return ".. I'm working"
