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

        #getting the voter count condition
        if kwargs['voter'] == 'count':

            count_qry = db_defs.Voter.query()
            count = count_qry.count(Limit=None)
            self.response.write("{ \"Voter Count\" : %d }" % (count))

        elif len(kwargs['voter']) > 4:

            get_var = kwargs['voter']

            #condition that a specific district was passed into get_var, not "all"

            if len(get_var) > 10:
                the_voter = db_defs.Voter.get_by_id(int(get_var))

                voter_dict = {int(the_voter.key.id()) : format_voter(the_voter)}

            self.response.write(json.dumps(voter_dict, indent=4))

    def post(self):

        #testing 
        #self.response.write("you just made a post to Voters.py with\nvoterID# %s\npassword: %s\n\n" % (self.request.get('id'), self.request.get('pass')))

        if not self.request.get('id'):
            self.response.write("Error, incorrect parameters")
            return

        #query the voter using the given voterID
        voter = idCheck(int(self.request.get('id')))

        #condition that just the id was entered (determines if voter exists)
        if not self.request.get('pass'):
            #testing
            #self.response.write("voter value: %s\n\n" % (str(voter)))

            if voter != None:
                self.response.write(json.dumps({ "ID_exists" :  True, "has_pass" : (voter.password != None) }))
            else:
                self.response.write(json.dumps({ "ID_exists" :  False }))

        #condition that id and password were both entered (ensure that password matches voterID)
        else:

            self.response.write(json.dumps({"VoterAuth": (voter.password == self.request.get('pass'))}))

    #create a single new voter or update an existing voter
    def put(self):

        #Error condition
        if not self.request.get('new'):
            self.response.write("Parameter Error")
            return

        #condition that this is new voter entry
        elif self.request.get('new') == 'True':

            #if new voter entry, id being used cannot already exist...throw error if it does
            if idCheck(int(self.request.get('id'))) != None:
                self.response.write("Error: id already exists")
                return

            newVoter = db_defs.Voter()


        #condition that this is updating entry of existing voter
        elif self.request.get('new') == 'False':

            #if updating voter entity, the id must exist....check that here
            newVoter = idCheck(int(self.request.get('id')))
            if newVoter == None:
                self.response.write("Error: id does not exist")
                return

            voter_key = newVoter.key.id()
            
        if self.request.get('party'):
            newVoter.party = self.request.get('party')

        if self.request.get('pass'):
            newVoter.password = self.request.get('pass')

        if self.request.get('age'):
            newVoter.age = int(self.request.get('age'))

        if self.request.get('education_lvl'):
            newVoter.education_lvl = int(self.request.get('education_lvl'))

        if self.request.get('ethnicity'):
            #test
            ethnicities = [int(ethnicity) for ethnicity in self.request.get('ethnicity').encode("utf-8").split(',')]
            #self.response.write("ethnicity received from http: %s\nethnicites is variable type: %s\n" % (ethnicities, type(ethnicities)))
            #return
            newVoter.ethnicity = ethnicities

        if self.request.get('income_lvl'):
            newVoter.income_lvl = int(self.request.get('income_lvl'))

        if self.request.get('sex'):
            newVoter.sex = str(self.request.get('sex')) == 'True'

        if self.request.get('id'):
            newVoter.voter_id = int(self.request.get('id'))

        #if this is new voter entity, the voter_key returned by put is new key...
        if self.request.get('new') == 'True':
            voter_key = newVoter.put()

        #but if the voter entity is being updated, ignore the value returned by put()
        elif self.request.get('new') == 'False':
            newVoter.put()

        self.response.write("voter_key = %s\n" % (str(voter_key)))

        

#decodes enumerated and abbreviated voter info into dict
def format_voter(voter):

    L = lists.Lists()

    voter_dict = voter.to_dict()

    #condition that voter has not yet submitted vote
    if voter.vote_key != None:
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

#checks if a particular voter.voter_id already exists, if not, returns None...if exists, returns the entity
def idCheck(theID):
    id_qry = db_defs.Voter.query(db_defs.Voter.voter_id == theID)
    return id_qry.get()