import webapp2
import base_page
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore
import db_defs

# Extends the base_page which was imported
class Admin(base_page.BaseHandler):
	def __init__(self, request, response):
		# Override the init function
		self.initialize(request, response)
		# Make sure we start with empty dictionary
		self.template_values = {}
		self.template_values['upload_url'] = blobstore.create_upload_url('/channel/add')

	# render in this file (admin.py)
	def render(self, page):
		# Python list comprehension
		# See database defintions: db_defs.py
		# ndb.Model has built-in query function
		# db_defs.Channel.query().fetch() returns a list of channels
		# For each x in that list, make a dictionary of name and urlsafe key of channel
		# urlsafe so we can pass it to a website without it being mangled by HTML encoding
		# We end up with a list of dictionaries (happening inside square brackets [])
		self.template_values['classes'] = [{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.ChannelClass.query().fetch()]
		self.template_values['channels'] = [{'name':x.name,'key':x.key.urlsafe()} for x in db_defs.Channel.query(ancestor=ndb.Key(db_defs.Channel, self.app.config.get('default-group'))).fetch()]
		# render in base_page.py
		base_page.BaseHandler.render(self, page, self.template_values)

	def get(self):
		self.render('admin.html')

	# Default icon_key is none (if not passed one)
	def post(self, icon_key=None):
		# action is the name of the hidden input in admin.html
		action = self.request.get('action')
		if action == 'add_channel':
			# Key([Type], [Identifier])
			# Type = Channel
			# Id = 'base-data' in main.py (could have just hardcoded instead of passing function)
			# Parent key for all of the channels
			k = ndb.Key(db_defs.Channel, self.app.config.get('default-group'))
			# New channel, call constructor for channel
			# Only way to guarantee consistency when updating is to have everything be descendants of the same parent
			# Knows everything in that group needs to be updated and retrieved as a group
			# It is possible to save a channel, attempt to immediately display it via call to fetch from database
			# and not get it back from the database because it has not propagated throughout the database yet
			# Put it all underneath the same parent key lets us get at it all at once
			# (at some point, it will be consistent but may not be right now)
			chan = db_defs.Channel(parent=k)
			# Set name of channel from form
			chan.name = self.request.get('channel-name')
			# Construct a key from a urlsafe string (does this for every checkbox we check)
			chan.classes = [ndb.Key(urlsafe=x) for x in self.request.get_all('classes[]')]
			chan.active = True
			# Set to passed in icon_key
			chan.icon = icon_key
			# Save the channel by returning the key to this specific instance of a channel
			chan.put()
			self.template_values['message'] = 'Added channel ' + chan.name + ' to the database.'
		elif action == 'add_class':
			k = ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))
			c = db_defs.ChannelClass(parent=k)
			c.name = self.request.get('class-name')
			c.put()
			self.template_values['message'] = 'Added class ' + c.name + ' to the database.'
		else:
			self.template_values['message'] = 'Action ' + action + ' is unknown.'

		# template_values['classes'] = db_defs.ChannelClass.query().fetch()
		self.template_values['classes'] = db_defs.ChannelClass.query(
			ancestor=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))).fetch()
		self.render('admin.html')
