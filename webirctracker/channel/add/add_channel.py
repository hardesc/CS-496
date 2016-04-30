import webapp2
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
import admin

class AddChannel(blobstore_handlers.BlobstoreUploadHandler):
		def post(self):
			upload_files = self.get_uploads('icon')
			# If there is something, grab the first one (should only ever be one)
			if upload_files != []:
				blob_info = upload_files[0]
				# Make new instance of Admin handler
				admin.Admin(self.request, self.response).post(icon_key=blob_info.key())
			else:
				admin.Admin(self.request, self.response).post()