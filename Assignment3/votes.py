import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
import json

class Votes(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here

    def get(self, **kwargs):


        if kwargs['vote'] == 'all':

            count_qry = db_defs.Vote.query()
            count = count_qry.count(Limit=None)
            self.response.write("{ 'Vote Count' : %d }" % (count))

        elif len(kwargs['vote']) > 4:

            get_var = kwargs['district']

            #condition that a specific district was passed into get_var, not "all"

            if len(get_var) > 10:
                the_district = db_defs.District.get_by_id(int(get_var))


                districts_dict = {str("%s District %d" % (the_district.state_key.get().abbr, the_district.number)) : dist_keys_to_ids(the_district)}

            elif len(get_var) == 2 or len(get_var) == 1:

                districts_dict = {}
                districts = db_defs.District.query(db_defs.District.number == int(get_var)).fetch()
                districts_dict = dist_list_to_dict(districts)

            elif kwargs['district'] == 'all':

                districts_dict = {}
                districts = db_defs.District.query().fetch()
                districts_dict['District'] = dist_list_to_dict(districts)

            self.response.write(json.dumps(districts_dict))

class Districts_by_State(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here

    def get(self, **kwargs):

        self.response.write("Districts_by_State Get: 'state' = %s\n" % (kwargs['state']))
        if kwargs['state']:
            get_var = kwargs['state']
            if len(get_var) == 2:

                the_state = db_defs.State.query(db_defs.State.abbr == get_var).fetch(1)[0]
                districts = db_defs.District.query(db_defs.District.state_key == the_state.key).fetch()

            elif len(get_var) > 2:

                the_state = db_defs.State.get_by_id(int(get_var))
                districts = [dist.get() for dist in the_state.dist_key_list]

            self.response.write(json.dumps(dist_list_to_dict(districts)))
        else:
            self.response.write("error")


def dist_keys_to_ids(district):

    district_dict = district.to_dict()

    district_dict['vote_key_list'] = [vote_key.id() for vote_key in district_dict['vote_key_list']]
    district_dict['state_key'] = district.state_key.id()
    district_dict['key'] = district.key.id()

    return district_dict

def dist_list_to_dict(districts):

    districts_dict = {}
    for district in districts:
        districts_dict[str("%s District %d" % (district.state_key.get().abbr, district.number))] = dist_keys_to_ids(district)

    return districts_dict