from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from bugs.models import Bug, Feature
from bugs.forms import BugForm, FeatureForm


def bug_report(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    page_heading = 'Report a bug'
    if request.method == "POST":
        bug_form = BugForm(request.POST)
        if bug_form.is_valid():
            bug_form.save(request.user)
            return HttpResponseRedirect(reverse('bug-list'))
    else:
        bug_form = BugForm()

    menu = {'parent': 'feedback'}            	
    return render(request, 'bug_report.html', {
                  'menu': menu,
                  'bug_form': bug_form,
                  'page_heading': page_heading,
                  })


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
            bug_form = BugForm(request.POST, instance=bug)
            if bug_form.is_valid():
                bug_form.save()
                return HttpResponseRedirect(reverse('bug-list'))
        else:
            bug_form = BugForm(instance=bug)
    else:
        display_mode = 'view'

    menu = {'parent': 'feedback'}            	
    return render(request, 'bug_edit.html', {
                  'menu': menu,
                  'display_mode': display_mode,
                  'bug': bug,
                  'bug_form': bug_form,
                  'page_heading': page_heading,
                  'allow_status_editing': allow_status_editing,
                  })


def bug_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    bugs = Bug.objects.all()
    page_heading = 'Bugs reported'
    table_headings = ('Bug number', 'Description', 'Date reported', 'Status')

    menu = {'parent': 'feedback'}            	
    return render(request, 'bug_list.html', {
                  'menu': menu,
                  'bugs': bugs,
                  'page_heading': page_heading,
                  'table_headings': table_headings,
                  })


def feature_request(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    page_heading = 'Request a feature/change'
    if request.method == "POST":
        feature_form = FeatureForm(request.POST)
        if feature_form.is_valid():
            feature_form.save(request.user)
        return HttpResponseRedirect(reverse('feature-list'))
    else:
        feature_form = FeatureForm()

    menu = {'parent': 'feedback'}            	
    return render(request, 'feature_request.html', {
                  'menu': menu,
                  'feature_form': feature_form,
                  'page_heading': page_heading,
                  })


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

    menu = {'parent': 'feedback'}            	
    return render(request, 'feature_edit.html', {
                  'menu': menu,
                  'display_mode': display_mode,
                  'feature': feature,
                  'feature_form': feature_form,
                  'page_heading': page_heading,
                  'allow_status_editing': allow_status_editing,
                  })


def feature_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))
    features = Feature.objects.all()
    page_heading = 'Features/changes requested'
    table_headings = ('Request number', 'Description', 'Date requested', 'Status',)

    menu = {'parent': 'feedback'}            	
    return render(request, 'feature_list.html', {
                  'menu': menu,
                  'features': features,
                  'page_heading': page_heading,
                  'table_headings': table_headings,
                  })

