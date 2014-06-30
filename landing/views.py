import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def example_agenda(request):
    path_to_pdf = os.path.join(settings.BASE_DIR, '../landing/pdfs/example_agenda.pdf')
    f = open(path_to_pdf, 'r')
    pdf_contents = f.read()
    f.close()
    
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=econvenor-example-agenda.pdf'
    return response
    

def example_minutes(request):
    path_to_pdf = os.path.join(settings.BASE_DIR, '../landing/pdfs/example_minutes.pdf')
    f = open(path_to_pdf, 'r')
    pdf_contents = f.read()
    f.close()
    
    response = HttpResponse(pdf_contents, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=econvenor-example-minutes.pdf'
    return response


def faqs(request):
    return render(request, 'landing_faqs.html')


def terms(request):
    return render(request, 'landing_terms.html')


def project(request):
    return render(request, 'landing_project.html')


def contact(request):
    return render(request, 'landing_contact.html')


def volunteer(request):
    return render(request, 'landing_volunteer.html')


def donate(request):
    return render(request, 'landing_donate.html')
