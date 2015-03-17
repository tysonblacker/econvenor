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


def questions(request):
    return render(request, 'questions.html')


def terms(request):
    return render(request, 'terms.html')


def project(request):
    return render(request, 'project.html')


def contact(request):
    return render(request, 'contact.html')


def volunteer(request):
    return render(request, 'volunteer.html')


def donate(request):
    return render(request, 'donate.html')


def source(request):
    return render(request, 'source.html')


def pricing(request):
    return render(request, 'pricing.html')


def hack(request):
    return render(request, 'hack.html')


def conduct(request):
    return render(request, 'conduct.html')
