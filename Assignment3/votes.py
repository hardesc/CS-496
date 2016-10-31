import webapp2
import base_page
from google.appengine.ext import ndb
import db_defs
import container_class_defs
import json
import lists

class Votes(base_page.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here

    def get(self, **kwargs):


        if kwargs['vote'] == 'all':

            count_qry = db_defs.Vote.query()
            count = count_qry.count(Limit=None)
            self.response.write("{ 'Vote Count' : %d }" % (count))

        elif len(kwargs['vote']) > 4:

            get_var = kwargs['vote']

            #condition that a specific district was passed into get_var, not "all"

            if len(get_var) > 10:
                the_vote = db_defs.Vote.get_by_id(int(get_var))

                vote_dict = {str("Vote# %d" % (the_vote.key.id())) : format_vote(the_vote)}

            self.response.write(json.dumps(vote_dict))


def format_vote(vote):

    L = lists.Lists()

    vote_dict = vote.to_dict()
    vote_dict['state_key'] = vote.state_key.id()
    vote_dict['dist_key'] = vote.dist_key.id()
    vote_dict['voter_key'] = vote.voter_key.id()

    for i, issue in enumerate(vote.issues):
        vote_dict['issues'][i] = L.issues_list[issue]

    vote_dict['candidate'] = L.candidate_list[vote.candidate]


    return vote_dict