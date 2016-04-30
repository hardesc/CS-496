import webapp2
import os
import jinja2

class BaseHandler(webapp2.RequestHandler):

	# @ means this is not a typical definition
	# cached_property means first time = calculate the value
	# after that, return value without calculating it (return stored value)
	@webapp2.cached_property
	def jinja2(self):
		# Read about these properties at http://jinja.pocoo.org/docs/dev/api/
		return jinja2.Environment(
		# os.path.dirname is the directory where __file__ is located (__file__ refers to base_page.py)
		# so that we can always find the 'templates' folder as long as __file__ is a sibling of 'templates'
		loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
		# Make escaping HTML characters easier
		extensions=['jinja2.ext.autoescape'],
		autoescape=True
		)

	# default to empty dictionary if do not supply template_variables
	def render(self, template, template_variables={}):
		template = self.jinja2.get_template(template)
		self.response.write(template.render(template_variables))