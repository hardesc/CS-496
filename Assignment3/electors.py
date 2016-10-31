import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
import json
import lists

class Electors(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here

    def get(self, **kwargs):


        if kwargs['elector'] == 'count':

            count_qry = db_defs.Electoral_College.query()
            count = count_qry.count(Limit=None)
            self.response.write("{ 'Elector Count' : %d }" % (count))
            return

        elif kwargs['elector'] == 'all':

            all_electors = db_defs.Electoral_College.query().fetch()
            
            elector_dict = {str("Elector# %d" % (the_elector.key.id())) : format_elector(the_elector) for the_elector in all_electors}



        elif len(kwargs['elector']) > 5:

            get_var = kwargs['elector']

            #condition that a specific district was passed into get_var, not "all"


            the_elector = db_defs.Electoral_College.get_by_id(int(get_var))

            elector_dict = {str("Elector# %d" % (the_elector.key.id())) : format_elector(the_elector)}

        self.response.write(json.dumps(elector_dict))


def format_elector(elector):

    L = lists.Lists()

    elector_dict = elector.to_dict()
    elector_dict['state_key'] = elector.state_key.id()
    elector_dict['candidate'] = L.candidate_list[elector.candidate]
    

    return elector_dict