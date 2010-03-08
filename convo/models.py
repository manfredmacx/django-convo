from django.db import models
from django.contrib.auth.models import User

class EntryManager(models.Manager):
	def get_convo(self):
		return self.filter(original=self)

class Entry(models.Model):
	original = models.ForeignKey('self', null=True, related_name="orginal_entry")
	parent = models.ForeignKey('self', null=True, related_name="parent_entry")
	title = models.CharField(max_length = 150)
	body = models.TextField(max_length = 4000)
	owner = models.ForeignKey(User, null=True)
	date_created = models.DateField(auto_now_add=True)
	
	objects = EntryManager()
	
	def __unicode__(self):
		return self.title
		
	def isOriginal(self):
		return self.original is None 	
		
	def userCanEdit(self, user):
		return (self.owner == user or (self.original is not None 
			and self.original.owner == user) or self.owner is None)

class Edit(models.Model):
	edit_by = models.ForeignKey(User)
	entry = models.ForeignKey(Entry)
	date_created = models.DateField(auto_now_add=True)
