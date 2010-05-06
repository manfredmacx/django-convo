from django import template
register = template.Library()

@register.filter
def mult(value, arg):
	if value is None:
		return arg
	return value * arg

import urllib, hashlib
from django.utils.translation import ugettext as _
from random import choice

class Gravatar(template.Node):
	def __init__(self, email_from_template):
		self.email = template.Variable(email_from_template)
	def render(self, context):
		default = choice(("identicon", "monsterid", "wavatar"))
		size = 55
		gravatar_url = "http://www.gravatar.com/avatar/"
		try:
			gravatar_url += hashlib.md5(self.email.resolve(context)).hexdigest() + "?"
		except:
			gravatar_url += "?"
		gravatar_url += urllib.urlencode({'d':default, 'size':str(size)})
		return gravatar_url		

def get_gravatar_url(parser, token):
	try:
		tag_name, email_from_template = token.split_contents()
	except ValueError:
		raise TemplateSyntaxError(
			_('tag requires exactly two arguments'))
	return Gravatar(email_from_template)
	
register.tag('get_gravatar_url', get_gravatar_url)
