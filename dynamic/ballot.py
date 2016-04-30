import webapp2
import base_page2
from google.appengine.ext import ndb
import db_defs

class Ballot(base_page2.BaseHandler):
    def get(self):
        self.render('/ballot.html')

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
        Issues.issues = self.request.get('issues').split()
        Issues.put()
        k4 = ndb.Key(db_defs.Email, 'Email')
        Email = db_defs.Email(parent=k4)
        Email.address = self.request.get('email')
        Email.put()
        k5 = ndb.Key(db_defs.Phone, 'Phone')
        Phone = db_defs.Phone(parent=k5)
        Phone.number = int(self.request.get('phone'))
        Phone.put()
        self.render('ballot.html', {'message':'You successfull cast your vote for ' + Candidate.name + '.'})
