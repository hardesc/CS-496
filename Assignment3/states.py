import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs

sunlight.config.API_KEY = 'a79f7eb00f544ba9a95a7001c8265966'

class States(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here

    def post(self):
    	key = ndb.Key(db_defs.State, 'States')
        State = db_defs.State(parent=key)

        #Using the post request variables, populate the members of Vote and enter it into the db as entity
        State.abbr = (self.request.get('abbr'))
        State.quant_districts = int(self.request.get('quant_districts'))
        State.quant_electors = int(self.request.get('quant_electors'))
        #State.dist_key_list = self.request.get('dist_key_list', allow_multiple=True)
        #State.elector_key_list = self.request.get('elector_key_list', allow_multiple=True,)

        #self.response.write('Wrote some stuff to database, ')
        State.put()
