from django import template
register = template.Library()

@register.filter
def mult(value, arg):
	if value is None:
		return arg
	return value * arg
