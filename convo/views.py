r""" 
	Default views
	Design pattern copied nearly verbatim from django-profile
	(http://code.google.com/p/django-profile/)
"""
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from convo import Convo
from convo.models import Entry, Edit

def add_new(request, nparent=None, form_class=None, success_url=None,
			template_name='convo/add_new.html',
			extra_context=None):
	""" Create a new Entry """
	if form_class is None:
		form_class = Convo.getForm()
	if success_url is None:
		success_url = "/"
	if request.method == 'POST':
		form = form_class(data=request.POST)
		if form.is_valid():
			en = form.save(commit=False)
			if request.user.is_authenticated():
				en.owner = request.user
			en.parent = nparent
			if nparent is None:
				en.original = None
			else:
				if nparent.original is None:
					en.original = nparent
				else:
					en.original = nparent.original
			en.save()
			return HttpResponseRedirect(success_url)
	else:
		form = form_class()
	if nparent is None:
		action_url = reverse('add_new_convo_entry')
	else:
		action_url = reverse('add_child_convo_entry', kwargs={"parent_id":nparent.id})    
	context = getContext(request, extra_context)   
	return render_to_response(template_name, { 'form': form, "action_url" : action_url }, context_instance=context)

def getContext(request, extra_context):
	""" Combine passed-in extra_context with RequestContext object """
	if extra_context is None:
		extra_context = {}
	context = RequestContext(request)
	for key, value in extra_context.items():
		context[key] = callable(value) and value() or value
	return context
	    
def add_child(request, parent_id, form_class=None, success_url=None,
			template_name='convo/add_new.html',
			extra_context=None):
	""" Create a new Entry that is the child of the passed-in Entry """
	parent = Entry.objects.get(pk=parent_id)
	return add_new(request, parent, form_class, success_url, template_name, extra_context)

def show_entry(request, e_id, template_name='convo/show.html', extra_context = None):
	""" Display an Entry """
	e = Entry.objects.get(pk=e_id)
	t = loader.get_template(template_name)
	if extra_context is None:
		extra_context = {}
	extra_context['entry_template'] = get_entry_template(request, e)
	c = getContext(request, extra_context)
	return HttpResponse(t.render(c))

def show_convo(request, e_id, template_name='convo/show_convo.html', extra_context = None):
	""" Display a threaded conversation """
	e = Entry.objects.get(pk=e_id)
	from convo import Convo
	es = Convo.getConvo(e)
	entries = []
	for en in es:
		entries.append(get_entry_template(request, en))	
	t = loader.get_template(template_name)
	if extra_context is None:
		extra_context = {}
	extra_context['entries'] = entries
	c = getContext(request, extra_context)
	return HttpResponse(t.render(c))

def get_entry_template(request, entry, template_name="convo/single_entry.html"):
	""" Return the rendered template for a single item """
	t = loader.get_template(template_name)
	c = RequestContext(request, {
		"editable" : request.user.is_authenticated() and entry.userCanEdit(request.user),
		"e" : entry,
		"edits" : entry.edit_set.select_related(),
	})
	return t.render(c)

@login_required	
def edit_entry(request, e_id, form_class=None, success_url=None,
				template_name='convo/edit.html', extra_context = None):
	""" Edit an Entry """
	e = Entry.objects.get(pk=e_id)
	if e.userCanEdit(request.user):
		if form_class is None:
			form_class = Convo.getForm()
		if success_url is None:
			success_url = "/"
		if request.method == 'POST':
			form = form_class(data=request.POST, instance=e)
			if form.is_valid():
				en = form.save()
				edit = Edit()
				edit.entry = en
				edit.edit_by = request.user
				edit.save()
			return HttpResponseRedirect(success_url)
		else:
			form = form_class(instance=e)   
		context = getContext(request, extra_context)   
		return render_to_response(template_name, { 'form': form, 'e' : e, }, context_instance=context)
	else:
		return HttpResponseRedirect("/")
		

	
