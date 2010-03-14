from django.db import models
from django.contrib.auth.models import User

class EntryManager(models.Manager):
	def get_convo(self, entry):
		""" return this object and all children """
		return self.filter(models.Q(original=entry) | models.Q(pk=entry.id))

class Entry(models.Model):
	original = models.ForeignKey('self', null=True, related_name="orginal_entry")
	parent = models.ForeignKey('self', null=True, related_name="parent_entry")
	title = models.CharField(max_length = 150)
	body = models.TextField(max_length = 4000)
	owner = models.ForeignKey(User, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	level = models.IntegerField()
	
	objects = EntryManager()
	
	def __unicode__(self):
		return self.title
		
	def isOriginal(self):
		return self.original is None 
			
	def getOriginal(self):	
		if self.isOriginal():
			return self
		else:
			return self.original
			
	def userCanEdit(self, user):
		return (self.owner == user or (self.isOriginal() 
			and self.original.owner == user) or self.owner is None)

	def save(self, *args, **kwargs):
		self.level = self.parent.level + 1 if self.parent is not None else 1
		super(Entry, self).save(*args, **kwargs)

class Edit(models.Model):
	edit_by = models.ForeignKey(User)
	entry = models.ForeignKey(Entry)
	date_created = models.DateField(auto_now_add=True)
