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
        base_page2.BaseHandler.render(self, 'ballot.html', self.template_values)

    def post(self):
        k1 = ndb.Key(db_defs.VoterID, 'VoterID')
        VoterID = db_defs.VoterID(parent=k1)
        VoterID.number = int(self.request.get('id'))
        VoterID.put()

        k2 = ndb.Key(db_defs.Candidate, 'Candidate')
        Candidate = db_defs.Candidate(parent=k2)
        Candidate.name = self.request.get('vote')
        Candidate.put()

        k3 = ndb.Key(db_defs.Issues, 'Issues')
        Issues = db_defs.Issues(parent=k3)
        Issues.issues = self.request.get('issues', allow_multiple=True)
        Issues.put()

        k4 = ndb.Key(db_defs.Email, 'Email')
        Email = db_defs.Email(parent=k4)
        Email.address = self.request.get('email')
        Email.put()

        k5 = ndb.Key(db_defs.Phone, 'Phone')
        Phone = db_defs.Phone(parent=k5)
        Phone.number = int(self.request.get('phone'))
        Phone.put()

        self.template_values['cast'] = True
        self.render('ballot.html')
        self.template_values['cast'] = False
