from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max

class EntryManager(models.Manager):
	def get_convo(self, entry):
		""" return this object and all children """
		return self.filter(models.Q(original=entry) | models.Q(pk=entry.id))
		
	def get_convo_last_modified(self, entry):
		return self.get_convo(entry).order_by('date_modified').reverse()[0]

class Entry(models.Model):
	original = models.ForeignKey('self', null=True, related_name="original_entry")
	parent = models.ForeignKey('self', null=True, related_name="parent_entry")
	title = models.CharField(max_length = 150)
	slug = models.SlugField(max_length=250, db_index=True, editable=False, unique=True)
	body = models.TextField(max_length = 4000)
	owner = models.ForeignKey(User, null=True)
	owner_if_anonymous = models.CharField(max_length = 150, null=True)
	url_if_anonymous = models.URLField(max_length = 1000, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	level = models.IntegerField()
	type = models.CharField(max_length=50, default="ALL")
	published = models.BooleanField(default=True)
	
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
		orig = self.getOriginal()
		own = self.owner or None
		return (own == user or orig.owner == user or own is None)
	
	def _child_count(self):
		return Entry.objects.filter(models.Q(original=self) | models.Q(pk=self.id)).count() - 1

	def save(self, *args, **kwargs):
		self.level = self.parent.level + 1 if self.parent is not None else 1
		i = 2
		while True:
			try:
				from django.template.defaultfilters import slugify
				from django.db import IntegrityError
				if not self.id:
					self.slug = slugify(self.title)
				super(Entry, self).save(*args, **kwargs)
			except IntegrityError:
				self.slug = slugify("-".join((self.title,str(i),)))
				try:
					super(Entry, self).save(*args, **kwargs)
				except IntegrityError:
					i += 1
				else:
					break
			else:
				break
		
	#TODO - needs to be generic
	def get_absolute_url(self):
		if self.type == "BLOG":
			return "/blog/{0}/{1}/{2}/{3}".format(self.date_created.year, self.date_created.month, self.date_created.day, self.slug)
		if self.type == "PAGE":
			return "/info/{0}".format(self.slug,)
		return "/social/{0}/convo".format(self.id)
			
	def _convo_last_mod_date(self):
		return self.objects.get_convo_last_modified(self).date_modified

	def __cmp__(self, other):
		return cmp(self.date_modified, other.date_modified)
		
	convo_last_mod_date = property(_convo_last_mod_date)
	child_count = property(_child_count)

class Edit(models.Model):
	edit_by = models.ForeignKey(User)
	entry = models.ForeignKey(Entry)
	date_created = models.DateField(auto_now_add=True)
