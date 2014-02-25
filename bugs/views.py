from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from core.models import Bug, Feature
from core.forms import BugForm, FeatureForm
from core.utils import save_and_add_owner


def bug_report(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Report a bug'
	if request.method == "POST":
		save_and_add_owner(request, BugForm(request.POST))
		return HttpResponseRedirect(reverse('bug-list'))
	else:
		bug_form = BugForm()
	return render_to_response('bug_report.html', {'user': request.user, 'bug_form': bug_form, 'page_heading': page_heading}, RequestContext(request))
	

def bug_edit(request, bug_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Bug report'
	administrator = 1
	allow_status_editing = False
	bug_form = {}
	bug = Bug.objects.get(pk=bug_id)
	if (request.user.id == administrator) or (request.user.id == int(bug.owner_id)):
		display_mode = 'edit'
		if request.user.id == administrator:
			allow_status_editing = True
		if request.method == "POST":
			save_and_add_owner(request, BugForm(request.POST, instance=bug))
			return HttpResponseRedirect(reverse('bug-list'))
		else:
			bug_form = BugForm(instance=bug)
	else:
		display_mode = 'view'
	return render_to_response('bug_edit.html', {'user': request.user, 'display_mode': display_mode, 'bug': bug, 'bug_form': bug_form, 'page_heading': page_heading, 'allow_status_editing': allow_status_editing}, RequestContext(request))
	

def bug_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	bugs = Bug.objects.all()
	page_heading = 'Bugs reported'
	table_headings = ('Bug number', 'Description', 'Date reported', 'Status')
	return render_to_response('bug_list.html', {'user': request.user, 'bugs': bugs, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))
	
	
def feature_request(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Request a feature/change'
	if request.method == "POST":
		save_and_add_owner(request, FeatureForm(request.POST))
		return HttpResponseRedirect(reverse('dashboard'))
	else:
		feature_form = FeatureForm()
	return render_to_response('feature_request.html', {'user': request.user, 'feature_form': feature_form, 'page_heading': page_heading}, RequestContext(request))
	

def feature_edit(request, feature_id):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	page_heading = 'Feature/change request'
	administrator = 1
	allow_status_editing = False
	feature_form = {}
	feature = Feature.objects.get(pk=feature_id)
	if (request.user.id == administrator) or (request.user.id == int(feature.owner_id)):
		display_mode = 'edit'
		if request.user.id == administrator:
			allow_status_editing = True
		if request.method == "POST":
			save_and_add_owner(request, FeatureForm(request.POST, instance=feature))
			return HttpResponseRedirect(reverse('feature-list'))
		else:
			feature_form = FeatureForm(instance=feature)
	else:
		display_mode = 'view'
	return render_to_response('feature_edit.html', {'user': request.user, 'display_mode': display_mode, 'feature': feature, 'feature_form': feature_form, 'page_heading': page_heading, 'allow_status_editing': allow_status_editing}, RequestContext(request))


def feature_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('index'))
	features = Feature.objects.all()
	page_heading = 'Features/changes requested'
	table_headings = ('Request number', 'Description', 'Date requested', 'Status',)
	return render_to_response('feature_list.html', {'user': request.user, 'features': features, 'page_heading': page_heading, 'table_headings': table_headings}, RequestContext(request))

