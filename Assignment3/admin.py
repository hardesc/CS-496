import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
from lists import Lists
import sys


class Admin(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response) #forgot why this is here

	def post(self):

		#===============================FULL DATABASE LOAD FROM SCRATCH==========================
		if self.request.get('fill_all') == 'True':

			self.nuke()#clear the entire db, since we're filling it from scratch

			#===============GENERATE AND GET ALL OUR LISTS------------------------
			L = Lists()
			container_class_defs.generate_all_states(L)
			container_class_defs.generate_all_districts(L)
			container_class_defs.generate_all_electoral_college(L)
			db_State_list = []
			key_list = []
									#==============STATES===============================
			#===================GET THE STATES FROM THE CONTAINERS AND PUT THEM IN THE DB============
			for i, our_state in enumerate(L.all_state_classes):

				key_list.append(ndb.Key(db_defs.State, 'States'))
				db_State_list.append(db_defs.State(parent=key_list[i]))

				db_State_list[i].abbr = our_state.abbr
				db_State_list[i].quant_districts = our_state.quant_districts
				db_State_list[i].quant_registered = our_state.quant_registered
				db_State_list[i].quant_electors = our_state.quant_electors
				#db_State_list[i].dist_key_list = []
				#db_State_list[i].elector_key_list = []

			state_keys = ndb.put_multi(db_State_list)#batch put all state keys in the db

			state_key_dict = {key.get().abbr: key for key in state_keys}#build a dict out of the state_keys list to use in District obj building
									#==============================DISTRICTS======================
			#============GET THE DISTRICTS FROM CONTAINERS, GET THEIR STATES, FILL STATE.DIST LISTS, PUT IN DB====
			db_Dist_list = []
			key_list = []

			for i, our_dist in enumerate(L.all_district_classes):

				key_list.append(ndb.Key(db_defs.District, 'Districts'))
				db_Dist_list.append(db_defs.District(parent=key_list[i]))

				db_Dist_list[i].number = our_dist.number
				db_Dist_list[i].state = state_key_dict[str(our_dist.state.abbr)]
				#db_Dist_list[i].voters = []

			dist_keys = ndb.put_multi(db_Dist_list)#batch put all district keys in the db, store the keys in dist_keys

			#===================================================STATES.DISTRICT_KEY_LISTS======================================
			#===============PUT A COPY OF EVERY NEWLY CREATED DISTRICT KEY IN IT'S PROPER STATE LIST IN THE DB=================
			#extracts state object from dist_key, assigne the dist_key as an element in the state's dist_key_list...just trust me

			
			state_dist_keys_dict = {}
			state_to_put_list = []
			for state_key in state_keys:
				dist_key_list = []
				for dist_key in dist_keys:
					if dist_key.get().state == state_key:
						state_dist_keys_dict[state_key] = dist_key_list.append(dist_key)

				state_dist_keys_dict[state_key] = dist_key_list
				state_to_put = state_key.get()
				state_to_put.dist_key_list = dist_key_list

				state_to_put_list.append(state_to_put)

				#state_to_put.put()
				#break

			ndb.put_multi(state_to_put_list)


	#============================================ELECTORAL_COLLEGE============================================
"""
			class Electoral_College(ndb.Model):
			evoter_id = ndb.IntegerProperty(required=True)
			state = ndb.KeyProperty(required=True)
			candidate = ndb.IntegerProperty(required=False)
"""				
			#============GET THE DISTRICTS FROM CONTAINERS, GET THEIR STATES, FILL STATE.DIST LISTS, PUT IN DB====
			db_Dist_list = []
			key_list = []

			for i, our_dist in enumerate(L.all_district_classes):

				key_list.append(ndb.Key(db_defs.District, 'Districts'))
				db_Dist_list.append(db_defs.District(parent=key_list[i]))

				db_Dist_list[i].number = our_dist.number
				db_Dist_list[i].state = state_key_dict[str(our_dist.state.abbr)]
				#db_Dist_list[i].voters = []

			dist_keys = ndb.put_multi(db_Dist_list)#batch put all district keys in the db, store the keys in dist_keys




	def delete(self):

		if self.request.get('nuke') == 'True':
			self.nuke()

	def get(self):

		if self.request.get('test')  == 'True':

			qry = db_defs.State.query()
			states = qry.fetch()

			for state in states:
				self.response.write("%s: " % (state.abbr))
				for i, dist in enumerate(state.dist_key_list):
					state_got = dist.get().state.get()
					self.response.write("%d) dist data: state = %s; number = %d\n" % (i, dist.get().state.get().abbr, dist.get().number))

	def nuke(self):

		state_qry = db_defs.State.query()
		qo = ndb.QueryOptions(keys_only=True)
		nuke_states = state_qry.fetch(51, options=qo)

		dist_qry = db_defs.District.query()
		qo = ndb.QueryOptions(keys_only=True)
		nuke_dists = dist_qry.fetch(433, options=qo)

		ndb.delete_multi(nuke_states)
		ndb.delete_multi(nuke_dists)
