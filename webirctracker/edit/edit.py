import webapp2
import base_page
from google.appengine.ext import ndb
from google.appengine.api import images
from google.appengine.ext import blobstore
import db_defs

class Edit(base_page.BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		self.template_values['edit_url'] = blobstore.create_upload_url( '/edit/channel' )

	def get(self):
		if self.request.get('type') == 'channel':
			# Pull the key and turn it into an ndb database key
			channel_key = ndb.Key(urlsafe=self.request.get('key'))
			# Now we have a channel object
			channel = channel_key.get()
			# If there is a channel icon, display it
			# Use images service to get the url for that icon
			# Pass blobkey for the image you want the url of
			if channel.icon:
				self.template_values['img_url'] = images.get_serving_url(channel.icon, crop=True, size=64)
			self.template_values['channel'] = channel
			# Get all classes that could be associated with the channel
			classes = db_defs.ChannelClass.query(ancestor=ndb.Key(db_defs.ChannelClass, self.app.config.get('default-group'))).fetch()
			class_boxes = []
			for c in classes:
				# If class is actually associated with the channel (checkmark)
				if c.key in channel.classes:
					class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':True})
				# Not associated (no checkmark)
				else:
					class_boxes.append({'name':c.name,'key':c.key.urlsafe(),'checked':False})
			self.template_values['classes'] = class_boxes
		# Display edit page
		self.render('edit.html', self.template_values)		
