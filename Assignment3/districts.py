import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
import json

class Districts(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response) #forgot why this is here

	def get(self, **kwargs):


		if self.request.get('test')  == 'True':

			qry = db_defs.District.query()
			districts = qry.fetch()

			for district in districts:
				self.response.write("%s: " % (district.abbr))
				for i, dist in enumerate(district.dist_key_list):
					district_got = dist.get().district.get()
					self.response.write("%d) dist data: district = %s; number = %d\n" % (i, dist.get().district.get().abbr, dist.get().number))

		elif self.request.get('count') == 'True':

			count_qry = db_defs.District.query()
			count = count_qry.count(Limit=None)
			self.response.write("{ 'District Count' : %d }" % (count))

		elif 'district' in kwargs:

			get_var = kwargs['district']

			#condition that a specific district was passed into get_var, not "all"
			if len(get_var) > 10 or len(get_var) <= 2:

				if len(get_var) > 10:
					the_district = db_defs.District.get_by_id(int(get_var))
				elif len(get_var) == 2:
					#self.response.write("the district: %s" % (the_district.get().abbr))
					#q = q.filter(MyModel._properties[kw] == v)
					#self.response.write("get_var = %s" % (get_var))

					q = db_defs.District.query(db_defs.District.abbr == get_var)
					#self.response.write("db_defs.District.abbr = %s\tget_var = %s" % (db_defs.District.abbr))
					the_district = q.fetch()[0]
				result = the_district.to_dict()
				#self.response.write(str(result))
				#return
				result['vote_key_list'] = [str(vote_key.id()) for vote_key in result['vote_key_list']]
				result['state_key'] = the_district.state_key.id()
				result['key'] = the_district.key.id()

				districts_dict = {str("%s District %d" % (the_district.state_key.get().abbr, the_district.number)) : result}
			#self.response.write(json.dumps(districts_dict))
			#self.response.write("Abbr: %s" % (district.abbr))



			elif kwargs['district'] == 'all':
			#elif self.request.get('all') == 'True':
				self.response.write("getting all districts\n")
				result_list = []
				districts_dict = {}

				districts_qry = db_defs.District.query()
				districts = districts_qry.fetch()
				#districts_dict = districts.to_dict()

				for district in districts:
					result_district_dict = {}
					district_dict  = {str("%s District %d" % (distrit.state_key.get().abbr, district.number)) : district.to_dict()}

					district_dict['vote_key_list'] = [vote_key.id() for vote_key in district_dict['vote_key_list']]
					district_dict['state_key'] = district.state_key.id()
					district_dict['key'] = district.key.id()

					result_district_dict[db_defs.State.get_by_id(int(district_dict['state_key'])).abbr] = district_dict

					result_list.append(result_district_dict)

				districts_dict['District'] = result_list


			self.response.write(json.dumps(districts_dict))