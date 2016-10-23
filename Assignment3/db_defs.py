from google.appengine.ext import ndb

class State(ndb.Model):
    abbr = ndb.StringProperty(required=True)
    quant_districts = ndb.IntegerProperty(required=True)
    quant_registered = ndb.IntegerProperty(required=True)
    quant_electors = ndb.IntegerProperty(required=True)
    dist_key_list = ndb.KeyProperty(repeated=True, write_empty_list=True)
    elector_key_list = ndb.KeyProperty(repeated=True, write_empty_list=True)

class District(ndb.Model):
	number = ndb.IntegerProperty(required=True)
	state = ndb.KeyProperty(required=True)
	voters = ndb.KeyProperty(repeated=True, write_empty_list=True)