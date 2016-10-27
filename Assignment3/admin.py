import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
from lists import Lists
import sys
import time
import json


class Admin(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response) #forgot why this is here

	def post(self):

		#===============================FULL DATABASE LOAD FROM SCRATCH==========================
		if self.request.get('fill_all') == 'True':

			self.nukeItAll()#clear the entire db, since we're filling it from scratch

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
				db_Dist_list[i].state_key = state_key_dict[str(our_dist.state.abbr)]
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
					if dist_key.get().state_key == state_key:
						state_dist_keys_dict[state_key] = dist_key_list.append(dist_key)

				state_dist_keys_dict[state_key] = dist_key_list
				state_to_put = state_key.get()
				state_to_put.dist_key_list = dist_key_list

				state_to_put_list.append(state_to_put)

				#state_to_put.put()
				#break

			ndb.put_multi(state_to_put_list)


	#============================================ELECTORAL_COLLEGE============================================
			#============GET THE DISTRICTS FROM CONTAINERS, GET THEIR STATES, FILL STATE.DIST LISTS, PUT IN DB====
			db_EC_list = []
			key_list = []

			for i, our_ec in enumerate(L.all_electoral_classes):

				key_list.append(ndb.Key(db_defs.Electoral_College, 'Electors'))
				db_EC_list.append(db_defs.Electoral_College(parent=key_list[i]))

				db_EC_list[i].evoter_id = our_ec.evoter_id
				db_EC_list[i].state_key = state_key_dict[str(our_ec.state.abbr)]

				if self.request.get('rand_ec_votes') == 'True':
					db_EC_list[i].candidate = our_ec.candidate
				#db_Dist_list[i].voters = []

			ec_keys = ndb.put_multi(db_EC_list)#batch put all district keys in the db, store the keys in dist_keys

			#===================================================STATES.ELECTORS_KEY_LISTS======================================
			#===============PUT A COPY OF EVERY NEWLY CREATED ELECTOR KEY IN IT'S PROPER STATE LIST IN THE DB=================
			#extracts state object from ec_key, assigne the ec_key as an element in the state's ec_key_list...just trust me

			
			state_ec_keys_dict = {}
			state_to_put_list = []
			for state_key in state_keys:
				ec_key_list = []
				for ec_key in ec_keys:
					if ec_key.get().state_key == state_key:
						state_ec_keys_dict[state_key] = ec_key_list.append(ec_key)

				state_ec_keys_dict[state_key] = ec_key_list
				state_to_put = state_key.get()
				state_to_put.elector_key_list = ec_key_list

				state_to_put_list.append(state_to_put)

				#state_to_put.put()
				#break

			ndb.put_multi(state_to_put_list)

			#============================================VOTERS============================================
			#=====================================GET THE VOTERS FROM CONTAINERS==========================
		if self.request.get('fill_votes') == 'True':
			if L not in locals():
				L = Lists()
			if self.request.get('rand_voters') == 'True':
				n = int(self.request.get('num'))
				container_class_defs.generateRandVoters(n, L)
				container_class_defs.generateRandVotes(L)

				db_voter_list = []
				key_list = []

				for i, voter in enumerate(L.all_voter_classes):

					key_list.append(ndb.Key(db_defs.Voter, 'Voters'))
					db_voter_list.append(db_defs.Voter(parent=key_list[i]))

					db_voter_list[i].voter_id = voter.id
					db_voter_list[i].party = voter.party
					db_voter_list[i].age = voter.age
					db_voter_list[i].sex = voter.sex == 'M'
					db_voter_list[i].income_lvl = voter.income_lvl
					db_voter_list[i].ethnicity = voter.ethnicity
					db_voter_list[i].education_lvl = voter.education_lvl

				future_voter_keys = ndb.put_multi_async(db_voter_list)#batch put all voter keys in the db

				voter_key_dict = {key.get_result().get().voter_id: key.get_result() for key in future_voter_keys}


				i = 0
				db_vote_list = []
				for i, vote in enumerate(L.all_vote_classes):

					key_list.append(ndb.Key(db_defs.Vote, 'Votes'))
					db_vote_list.append(db_defs.Vote(parent=key_list[i]))

					
					db_vote_list[i].voter_key = voter_key_dict[vote.voter_id]
					db_vote_list[i].candidate = vote.candidate
					db_vote_list[i].issues = vote.issues
					db_vote_list[i].state_key = state_key_dict[vote.state]
					
					#self.response.write("State %d:\ntype: %s\n\n" % (i, type(db_vote_list[i].state, quant_districts)))
					dist_key_list = []
					dist_key_list = state_dist_keys_dict[db_vote_list[i].state_key]
					for dist in dist_key_list:
						if dist.get().number == vote.district:
							db_vote_list[i].dist_key = dist

				future_vote_key_list = ndb.put_multi_async(db_vote_list)

				#===================================PUT ALL VOTE_KEYS IN VOTERS==================================================
				db_voter_list = []
				for vote_key in future_vote_key_list:
					vote_key.get_result().get().voter_key.get().vote_key = vote_key.get_result()
					db_voter_list.append(vote_key.get_result().get().voter_key.get())

					self.response.write("Voter id: %d\n" % (db_voter_list[-1].voter_id))

				#time.sleep(30)
				future_voter_key_list = ndb.put_multi(db_voter_list)

				#===================================PUT ALL VOTER_KEYS IN DISTRICTS==================================================
				"""
				state_key_dict
				state_dist_keys_dict
				"""

				dist_vote_keys_dict = {}
				dist_to_put_list = []
				for dist_key in dist_keys:
					vote_key_list = []
					for vote_key in future_vote_key_list:
						if vote_key.get_result().get().dist_key == dist_key:
							dist_vote_keys_dict[dist_key] = vote_key_list.append(vote_key.get_result())

					dist_vote_keys_dict[dist_key] = vote_key_list
					dist_to_put = dist_key.get()
					dist_to_put.vote_key_list = vote_key_list

					dist_to_put_list.append(dist_to_put)

					#state_to_put.put()
					#break

				ndb.put_multi(dist_to_put_list)




	def delete(self):

		if self.request.get('nuke') == 'True':
			self.nukeItAll()

	
				

	def nukeItAll(self):

		self.nuke(db_defs.State)
		self.nuke(db_defs.District)
		self.nuke(db_defs.Electoral_College)
		self.nuke(db_defs.Vote)
		self.nuke(db_defs.Voter)

	def nuke(self, Entity):
		Entity_qry = Entity.query()
		qo = ndb.QueryOptions(keys_only=True)
		ent_count = Entity_qry.count(limit=None, options=qo)
		if (ent_count):
			ndb.delete_multi(Entity_qry.fetch(ent_count, options=qo))
