import webapp2
import base_page2
from google.appengine.ext import ndb
import db_defs
import ballot

class Votes(base_page2.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here
        self.template_values = {}

    #refefines render from base_page2.BaseHandler to include template variables when data has been entered.
    #gets each database entry and stores them as template variables, calls render with template variables
    def render(self, page):
        """vote_list = []
        i = 0
        for vq in db_defs.Vote.query().fetch():

            vote = votes(vq.VID, vq.candidate, vq.issues, vq.email, vq.phone, vq.key.urlsafe())
            self.template_values['votes'] = vote_list.append(vote)
"""

        self.template_values['votes'] = [{'VID':vq.VID, 'candidate':vq.candidate, 'issues':vq.issues, 'email':vq.email, 'phone':vq.phone, 'key':vq.key.urlsafe()} for vq in db_defs.Vote.query().fetch()]

            #self.template_values['id'] = {'number':vq.VID, 'key':vq.key.urlsafe()}
            #self.template_values['Vote' + str(i)] = vote
            #i += 1

        #self.template_values['key'] = [vq.key.urlsafe()]
        """
        self.template_values['id'] = [{'number':vq.VID, 'key':vq.key.urlsafe()} for vq in db_defs.Vote.query().fetch()]
        self.template_values['candidate'] = [{'name':vq.candidate, 'key':vq.key.urlsafe()} for vq in db_defs.Vote.query().fetch()]
        self.template_values['issues'] = [{'name':vq.issues, 'key':vq.key.urlsafe()} for vq in db_defs.Vote.query().fetch()]
        self.template_values['email'] = [{'address':vq.email, 'key':vq.key.urlsafe()} for vq in db_defs.Vote.query().fetch()]
        self.template_values['phone'] = [{'number':vq.phone, 'key':vq.key.urlsafe()} for vq in db_defs.Vote.query().fetch()]
        """
        base_page2.BaseHandler.render(self, page, self.template_values)
        
    #don't actually know why this is necessary, if it is at all
    def get(self):
        self.template_values['cast'] = False
        base_page2.BaseHandler.render(self, 'votes.html', Ballot.template_values)

    def post(self):

        self.render('votes.html')

class votes:
    def __init__(self, id, candidate, issues, email, phone, key):
        self.id = id
        self.candidate = candidate
        self.issues = issues
        """for issue in issues:
            self.issues.append(issue)"""
        self.email = email
        self.phone = phone
        self.key = key
