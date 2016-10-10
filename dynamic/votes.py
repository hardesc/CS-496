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

        self.template_values['votes'] = [{'VID':vq.VID, 'candidate':vq.candidate, 'issues':vq.issues, 'email':vq.email, 'phone':vq.phone, 'key':vq.key.urlsafe()} for vq in db_defs.Vote.query().fetch()]

        base_page2.BaseHandler.render(self, page, self.template_values)
        
    #don't actually know why this is necessary, if it is at all
    def get(self):
        self.template_values['cast'] = False

        if self.request.get('delete') == 'true':
            url_key = self.request.get('key')
            delete_key = ndb.Key(urlsafe=url_key)
            delete_vote = delete_key.get()
            delete_vote.key.delete()


        self.render('votes.html')

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
