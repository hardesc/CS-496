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
	state_key = ndb.KeyProperty(required=True)
	vote_key_list = ndb.KeyProperty(repeated=True, write_empty_list=True)

class Electoral_College(ndb.Model):
	evoter_id = ndb.IntegerProperty(required=True)
	state_key = ndb.KeyProperty(required=True)
	candidate = ndb.IntegerProperty(required=False)


class Vote(ndb.Model):
	voter_key = ndb.KeyProperty(required=True)#must be changed to true after testing complete
	candidate = ndb.IntegerProperty(required=True)
	issues = ndb.IntegerProperty(repeated=True)
	dist_key = ndb.KeyProperty(required=False)
	state_key = ndb.KeyProperty(required=False)


class Voter(ndb.Model):
	voter_id = ndb.IntegerProperty(required=True)
	vote_key = ndb.KeyProperty(required=False)
	party = ndb.StringProperty(required=True)
	age = ndb.IntegerProperty(required=True)
	sex = ndb.BooleanProperty(required=True)
	income_lvl = ndb.IntegerProperty(required=True)
	ethnicity = ndb.IntegerProperty(repeated=True)
	education_lvl = ndb.IntegerProperty(required=True)
	password = ndb.StringProperty(required=False)
