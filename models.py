from google.appengine.ext import ndb


class User(ndb.Model):
    email = ndb.StringProperty()