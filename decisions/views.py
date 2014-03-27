from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from decisions.models import Decision
from utilities.commonutils import get_current_group


def decision_list(request):
    group = get_current_group(request)
    if group == None:	
        return HttpResponseRedirect(reverse('index'))

    decisions = Decision.objects.filter(group=group)
    table_headings = ('Meeting no',
                      'Item no',
                      'Decision',
                      )

    menu = {'parent': 'decisions', 'child': 'all_decisions'}    
    return render(request, 'decision_list.html', {
                  'menu': menu,
                  'decisions': decisions,
                  'table_headings': table_headings,
                  })
