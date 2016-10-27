import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
import json

class States(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response) #forgot why this is here

	def get(self):

		if self.request.get('test')  == 'True':

			qry = db_defs.State.query()
			states = qry.fetch()

			for state in states:
				self.response.write("%s: " % (state.abbr))
				for i, dist in enumerate(state.dist_key_list):
					state_got = dist.get().state.get()
					self.response.write("%d) dist data: state = %s; number = %d\n" % (i, dist.get().state.get().abbr, dist.get().number))

		elif self.request.get('count') == 'True':

			count_qry = db_defs.Vote.query()
			count = count_qry.count(Limit=None)
			self.response.write("{ 'Vote Count' : %d }" % (count))

		elif self.request.get('state'):

			get_var = self.request.get('state')

			#condition that a specific state was passed into get_var, not "all"
			if len(get_var) > 3 or len(get_var) == 2:

				if len(get_var) > 3:
					the_state = db_defs.State.get_by_id(int(get_var))
				elif len(get_var) == 2:
					#self.response.write("the state: %s" % (the_state.get().abbr))
					#q = q.filter(MyModel._properties[kw] == v)
					#self.response.write("get_var = %s" % (get_var))

					q = db_defs.State.query(db_defs.State.abbr == get_var)
					#self.response.write("db_defs.State.abbr = %s\tget_var = %s" % (db_defs.State.abbr))
					the_state = q.fetch()[0]
				result = the_state.to_dict()
				#self.response.write(str(result))
				#return
				result['elector_key_list'] = [str(elector_key.id()) for elector_key in result['elector_key_list']]
				result['dist_key_list'] = [str(dist_key.id()) for dist_key in result['dist_key_list']]
				result['key'] = the_state.key.id()

				states_dict = {the_state.abbr : result}
			#self.response.write(json.dumps(states_dict))
			#self.response.write("Abbr: %s" % (state.abbr))



		elif self.request.get('all') == 'True':

			result_list = []
			states_dict = {}

			states_qry = db_defs.State.query()
			states = states_qry.fetch()
			#states_dict = states.to_dict()

			for state in states:
				result_state_dict = {}
				state_dict  = state.to_dict()

				state_dict['elector_key_list'] = [elector_key.urlsafe() for elector_key in state_dict['elector_key_list']]
				state_dict['dist_key_list'] = [dist_key.urlsafe() for dist_key in state_dict['dist_key_list']]
				state_dict['key'] = state.key.urlsafe()

				result_state_dict[state_dict['abbr']] = state_dict

				result_list.append(result_state_dict)

			states_dict['State'] = result_list

		self.response.write(json.dumps(states_dict))