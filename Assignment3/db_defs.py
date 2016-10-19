from google.appengine.ext import ndb

class State(ndb.Model):
    abbr = ndb.StringProperty(required=True)
    quant_districts = ndb.IntegerProperty(required=True)
    quant_electors = ndb.IntegerProperty(required=True)
    dist_key_list = ndb.KeyProperty(repeated=True, write_empty_list=True)
    elector_key_list = ndb.KeyProperty(repeated=True, write_empty_list=True)
