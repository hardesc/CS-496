import webapp2

# Arbitary name of 'base-data'
config = {'default-group':'base-data'}

application = webapp2.WSGIApplication([
	('/edit/channel', 'edit_channel.EditChannel'),
	('/edit', 'edit.Edit'),
	('/channel/add', 'add_channel.AddChannel'),
	('/admin', 'admin.Admin'),
	('/', 'base_page.BaseHandler'),
], debug=True, config=config)