import webapp2
import os

class BaseHandler(webapp2.RequestHandler):

    def get(self):
        self.response.write('here\'s a list of urls for your dumb ass\n\nhttp://localhost:13080/states')
        
        