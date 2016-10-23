import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
from lists import Lists

class States(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response) #forgot why this is here

	def post(self):
		self.response.write("this is a post\n\n")

		#Fill the states entity with pre loaded state values derived from json from api calls
		if self.request.get('fill_all') == 'True':

			L = Lists()
			container_class_defs.generate_all_states(L)
			db_State_list = []
			key_list = []

			for i, our_state in enumerate(L.all_state_classes):

				key_list.append(ndb.Key(db_defs.State, 'States'))
				db_State_list.append(db_defs.State(parent=key_list[i]))

				db_State_list[i].abbr = our_state.abbr
				db_State_list[i].quant_districts = our_state.quant_districts
				db_State_list[i].quant_registered = our_state.quant_registered
				db_State_list[i].quant_electors = our_state.quant_electors
				db_State_list[i].dist_key_list = []
				db_State_list[i].elector_key_list = []

				#db_State_list.append(db_State)

			#db_State.put()
			ndb.put_multi(db_State_list)


"""
			else:
				#Using the post request variables, populate the members of Vote and enter it into the db as entity
				db_State.abbr = (self.request.get('abbr'))
				db_State.quant_districts = int(self.request.get('quant_districts'))
				db_State.quant_electors = int(self.request.get('quant_electors'))
				#db_State.dist_key_list = self.request.get('dist_key_list', allow_multiple=True)
				#db_State.elector_key_list = self.request.get('elector_key_list', allow_multiple=True,)

				#self.response.write('Wrote some stuff to database, ')
				db_State.put()
			"""
class Districts(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response) #forgot why this is here

	def post(self):
		self.response.write("this is a district post\n\n")

		#Fill the states entity with pre loaded state values derived from json from api calls
		if self.request.get('fill_all') == 'True':

			L = Lists()
			container_class_defs.generate_all_states(L)
			container_class_defs.generate_all_districts(L)
			db_Dist_list = []
			key_list = []

			for i in range(0, 1):#, our_dist in enumerate(L.all_district_classes):

				key_list.append(ndb.Key(db_defs.District, 'Districts'))
				db_Dist_list.append(db_defs.State(parent=key_list[i]))

				our_dist = L.all_district_classes[i]

				db_Dist_list[i].number = our_dist.number
				db_Dist_list[i].state = our_dist.state
				db_Dist_list[i].voters = []

				#db_Dist_list.append(db_State)

			db_Dist_list[i].put()
			#ndb.put_multi(db_Dist_list)
			self.response.write("db writing complete\n\n")