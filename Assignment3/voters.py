import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
import json
import lists

class Voters(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here

    def get(self, **kwargs):


        if kwargs['voter'] == 'all':

            count_qry = db_defs.Voter.query()
            count = count_qry.count(Limit=None)
            self.response.write("{ 'Voter Count' : %d }" % (count))

        elif len(kwargs['voter']) > 4:

            get_var = kwargs['voter']

            #condition that a specific district was passed into get_var, not "all"

            if len(get_var) > 10:
                the_voter = db_defs.Voter.get_by_id(int(get_var))

                voter_dict = {str("Voter# %d" % (the_voter.key.id())) : format_voter(the_voter)}

            self.response.write(json.dumps(voter_dict))


def format_voter(voter):

    L = lists.Lists()

    voter_dict = voter.to_dict()
    voter_dict['vote_key'] = voter.vote_key.id()


    for i, ethnicity in enumerate(voter.ethnicity):
        voter_dict['ethnicity'][i] = L.ethnicity_list[ethnicity]

    voter_dict['income_lvl'] = L.income_list[voter.income_lvl]
    voter_dict['education_lvl'] = L.education_lvl_list[voter.education_lvl]
    if voter_dict['sex']:
        voter_dict['sex'] = 'Male'
    else:
        voter_dict['sex'] = 'Female'


    return voter_dict