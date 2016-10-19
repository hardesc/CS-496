from google.appengine.ext import ndb

class Vote(ndb.Model):
    VID = ndb.IntegerProperty(required=True)
    candidate = ndb.StringProperty(required=True)
    issues = ndb.StringProperty(repeated=True)
    email = ndb.StringProperty(required=False)
    phone = ndb.IntegerProperty(required=False)
