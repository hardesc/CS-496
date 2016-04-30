from google.appengine.ext import ndb

class VoterID(ndb.Model):
    number = ndb.IntegerProperty(required=True)

class Candidate(ndb.Model):
    name = ndb.StringProperty(required=True)

class Issues(ndb.Model):
    issues = ndb.StringProperty(repeated=True)

class Email(ndb.Model):
    address = ndb.StringProperty(required=False)

class Phone(ndb.Model):
    number = ndb.IntegerProperty(required=False)
