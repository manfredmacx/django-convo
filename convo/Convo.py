"""
	Util class
"""
from django.forms import ModelForm
from models import Entry

def getForm():
	""" If no form is passed in to new/edit views, use this one """
	class _Form(ModelForm):
		class Meta:
			model = Entry
			fields = ('title', 'body',)
	return _Form
