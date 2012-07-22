import os
import google.appengine.api.app_identity as identity
import sys

# Read the GIT commit string.
GIT_VERSION = open('version.txt').read()

IS_DEV = os.environ['SERVER_SOFTWARE'].startswith("Dev")

if os.environ.has_key("HTTPS"):
    HTTP_TRANSPORT = "https"
else:
    HTTP_TRANSPORT = "http"

RUN_APP_STATS = True

if IS_DEV:
    WWWROOT = "http://localhost:8888"
else:
    WWWROOT = "%s://%s" % (HTTP_TRANSPORT, '%s.appspot.com' % identity.get_application_id())

# AppEngine email from address.
EMAIL_FROM = "system@%s.appspotmail.com"

FACEBOOK_CHANNEL_URL = "%s/%s" % (WWWROOT, "channel")
# Application name used for headers and other various areas.
APP_NAME = "WhiteRabbit"

# Place the app in debug mode.
APP_DEBUG = True
NAVBAR_ITEMS = {
    "/": "Home",
    "/_ah/admin": "Admin"
}

# Session backend.  Memcache is fast, but has a slight risk of losing a session.
SESSION_BACKEND = "memcache"

webapp2_config = {}
webapp2_config['webapp2_extras.sessions'] = {
    'secret_key': 'jdhfgisbru34u4bu5b4bu'
}
webapp2_config["webapp2_extras.jinja2"] = {
    "template_path": os.path.dirname(__file__)
}
