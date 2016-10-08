import webapp2
import base_page2
from google.appengine.ext import ndb
import db_defs

class Votes(base_page2.BaseHandler):
    def __init__(self, request, response):
        self.initialize(request, response) #forgot why this is here
        self.template_values = {}

    #refefines render from base_page2.BaseHandler to include template variables when data has been entered.
    #gets each database entry and stores them as template variables, calls render with template variables
    def render(self, page):
        idq = db_defs.VoterID.query().fetch()[0]
        self.template_values['id'] = {'number':idq.number, 'key':idq.key.urlsafe()}

        cq = db_defs.Candidate.query().fetch()[0]
        self.template_values['candidate'] = {'name':cq.name, 'key':cq.key.urlsafe()}

        #self.template_values['issues'] = [{'name':issq.issues, 'key':issq.key.urlsafe()} for issq in db_defs.Issues.query().fetch()]

        isq = db_defs.Issues.query().fetch()[-1]
        self.template_values['issues'] = {'name':isq.issues, 'key':isq.key.urlsafe()}

        eq = db_defs.Email.query().fetch()[0]
        self.template_values['email'] = {'address':eq.address, 'key':eq.key.urlsafe()}

        pq = db_defs.Phone.query().fetch()[0]
        self.template_values['phone'] = {'number':pq.number, 'key':pq.key.urlsafe()}

        base_page2.BaseHandler.render(self, page, self.template_values)

    #don't actually know why this is necessary, if it is at all
    def get(self):
        self.template_values['cast'] = False
        base_page2.BaseHandler.render(self, 'votes.html', self.template_values)

    def post(self):

        self.render('votes.html')
