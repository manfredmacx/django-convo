from django.contrib import admin
from convo.models import Entry

class EntryAdmin(admin.ModelAdmin):
	list_display = ('title', 'owner', 'owner_if_anonymous', 'parent')
	list_filter = ('type',)

admin.site.register(Entry, EntryAdmin)
