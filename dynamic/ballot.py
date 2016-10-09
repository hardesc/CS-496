import webapp2
import base_page2
from google.appengine.ext import ndb
import db_defs

class Ballot(base_page2.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here
        self.template_values = {}

    #refefines render from base_page2.BaseHandler to include template variables when data has been entered.
    #gets each database entry and stores them as template variables, calls render with template variables
    def render(self, page):
        vq = db_defs.Vote.query().fetch()[-1]
        self.template_values['id'] = {'number':vq.VID, 'key':vq.key.urlsafe()}
        self.template_values['candidate'] = {'name':vq.candidate, 'key':vq.key.urlsafe()}
        self.template_values['issues'] = {'name':vq.issues, 'key':vq.key.urlsafe()}
        self.template_values['email'] = {'address':vq.email, 'key':vq.key.urlsafe()}
        self.template_values['phone'] = {'number':vq.phone, 'key':vq.key.urlsafe()}

        base_page2.BaseHandler.render(self, page, self.template_values)

    #don't actually know why this is necessary, if it is at all
    def get(self):
        self.template_values['cast'] = False
        base_page2.BaseHandler.render(self, 'ballot.html', self.template_values)

    def post(self):
        key = ndb.Key(db_defs.Vote, 'Vote')
        Vote = db_defs.Vote(parent=key)
        Vote.VID = int(self.request.get('id'))
        Vote.candidate = self.request.get('vote')
        Vote.issues = self.request.get('issues', allow_multiple=True)     
        Vote.email = self.request.get('email')
        Vote.phone = int(self.request.get('phone'))
        Vote.put()

        self.template_values['cast'] = True
        self.render('ballot.html')
        self.template_values['cast'] = False
