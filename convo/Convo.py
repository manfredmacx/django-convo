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
			
	return _Form

def getConvo(entry):
	""" return list containing a sorted Entry thread """
	sorted = []
	original = entry.getOriginal()
	sorted.append(original)
	sorted.extend(__sortConvo(Entry.objects.filter(parent=original)))
	return sorted
	
def __sortConvo(children):
	""" Private function:  Sorts a queryset (or list) of Entries """
	sorted = []
	for c in children:
		sorted.append(c)
		sorted.extend(__sortConvo(Entry.objects.filter(parent=c)))
	return sorted
