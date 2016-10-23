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
		self.response.write("this is a post\n\n")

		if self.request.get('fill_all') == 'True':

			L = Lists()
			container_class_defs.generate_all_states(L)
			container_class_defs.generate_all_districts(L)
			container_class_defs.generate_all_electoral_college(L)
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
			state_keys = ndb.put_multi(db_State_list)

			key_dict = {key.get().abbr: key for key in state_keys}


			db_Dist_list = []
			key_list = []

			for i, key in enumerate(key_dict.keys()):
				self.response.write("%d.)%s : %s\n" % (i, key, key_dict[key]))

			for i, our_dist in enumerate(L.all_district_classes):
				"""if i > 10:
					break"""
				key_list.append(ndb.Key(db_defs.District, 'Districts'))
				db_Dist_list.append(db_defs.District(parent=key_list[i]))


				#our_dist = L.all_district_classes[i]

				assert type(our_dist.number) is int
				db_Dist_list[i].number = our_dist.number


				assert str(our_dist.state.abbr) in key_dict
				db_Dist_list[i].state = key_dict[str(our_dist.state.abbr)]

				self.response.write("db_Dist_list[%d].state = %s\tkey_dict[str(our_dist.state.abbr)] = %s" % (i, db_Dist_list[i].state, key_dict[str(our_dist.state.abbr)]))
				assert (type(db_Dist_list[i].state) == type(key_dict[str(our_dist.state.abbr)]))

				db_Dist_list[i].voters = []

				#db_Dist_list.append(db_Dist_list[i])

				#db_Dist_list[i].put()
			ndb.put_multi(db_Dist_list)
			self.response.write("db writing complete\n\n")

	def delete(self):
		self.response.write("this is a delete\n\n")

		if self.request.get('nuke') == 'True':
			self.nuke()

	def nuke(self):
		self.response.write("nuking\n\n")

		state_qry = db_defs.State.query()
		qo = ndb.QueryOptions(keys_only=True)
		nuke_states = state_qry.fetch(51, options=qo)

		dist_qry = db_defs.District.query()
		qo = ndb.QueryOptions(keys_only=True)
		nuke_dists = dist_qry.fetch(433, options=qo)

		#ndb.delete_multi(nuke_states)
		ndb.delete_multi(nuke_dists)
