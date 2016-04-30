from google.appengine.ext import ndb

class Message(ndb.Model):
	channel = ndb.StringProperty(required=True)
	date_time = ndb.DateTimeProperty(required=True)
	count = ndb.IntegerProperty(required=True)

class Channel(ndb.Model):
	name = ndb.StringProperty(required=True)
	# Repeated strings/list of keys
	# Repeated, not required, empty key is fine
	classes = ndb.KeyProperty(repeated=True)
	active = ndb.BooleanProperty(required=True)
	icon = ndb.BlobKeyProperty()

class ChannelClass(ndb.Model):
	name = ndb.StringProperty(required=True)