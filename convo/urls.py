from django.conf.urls.defaults import *
from convo import views

urlpatterns = patterns('',	
	url(r'^new/$', views.add_new, name='add_new_convo_entry'),
	url(r'^(?P<parent_id>\d+)/new/$', views.add_child, name='add_child_convo_entry'),
	url(r'^(?P<e_id>\d+)/edit/$', views.edit_entry, name='edit_convo_entry'),
	url(r'^(?P<e_id>\d+)/$', views.show_entry, name='show_convo_entry'),
)
