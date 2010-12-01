"""
	Util class
"""
from django.forms import ModelForm, CharField, URLField
from django.db import models
from models import Entry

def getForm(user):
	""" If no form is passed in to new/edit views, use this one """
	class _Form(ModelForm):
		class Meta:
			model = Entry
			fields = ('title', 'body',)
		def save(self, force_insert=False, force_update=False, commit=True):
			m = super(ModelForm, self).save(commit=False)
			from bleach import Bleach
			TAGS = ['b', 'em', 'i', 'strong', 'br', 'li', 'ul', 'ol', 'p', 'span']
			bl = Bleach()
			m.title = bl.clean(self.cleaned_data['title'])
			m.body = bl.clean(self.cleaned_data['body'], tags=TAGS)
			if commit:
				m.save()
			return m
	class _AdminForm(ModelForm):
		class Meta:
			model = Entry
			fields = ('title', 'body',)
		def save(self, force_insert=False, force_update=False, commit=True):
			m = super(ModelForm, self).save(commit=False)
			from bleach import Bleach
			TAGS = ['b', 'em', 'i', 'strong', 'br', 'li', 'ul', 'ol', 'p', 'span', 'a']
			bl = Bleach()
			m.title = bl.clean(self.cleaned_data['title'])
			m.body = bl.clean(self.cleaned_data['body'], tags=TAGS)
			if commit:
				m.save()
			return m
	class _AnonForm(ModelForm):
		owner_if_anonymous = CharField(max_length = 150, label="Name")
		url_if_anonymous = URLField(max_length=1000, label="URL", required=False)
		class Meta:
			model = Entry
			fields = ('title', 'owner_if_anonymous', 'url_if_anonymous', 'body')
		def save(self, force_insert=False, force_update=False, commit=True):
			m = super(ModelForm, self).save(commit=False)
			from bleach import Bleach
			TAGS = ['b', 'em', 'i', 'strong', 'br', 'li', 'ul', 'ol', 'p', 'span']
			bl = Bleach()
			m.title = bl.clean(self.cleaned_data['title'])
			m.body = bl.clean(self.cleaned_data['body'], tags=TAGS)
			if commit:
				m.save()
			return m
	if user.is_staff:
		return _AdminForm
	if user.is_authenticated():
		return _Form
	return _AnonForm

def getConvo(entry):
	s, t = getConvoWithTitle(entry)
	return s
	
def getConvoWithTitle(entry):
	""" return list containing a sorted Entry thread """
	sorted = []
	original = entry.getOriginal()
	sorted.append(original)
	sorted.extend(__sortConvo(Entry.objects.filter(parent=original)))
	return sorted, original.title
	
def __sortConvo(children):
	""" Private function:  Sorts a queryset (or list) of Entries """
	sorted = []
	for c in children:
		sorted.append(c)
		sorted.extend(__sortConvo(Entry.objects.filter(parent=c)))
	return sorted
