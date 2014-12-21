from django.shortcuts import render

from utilities.commonutils import set_path


def quick_start_guide(request):

    menu = {'parent': 'help'}            	         
    return render(request, 'quick_start_guide.html', {
                  'menu': menu,
    })


def user_guide(request):

    menu = {'parent': 'help'}            	         
    return render(request, 'user_guide.html', {
                  'menu': menu,
    })


def qanda(request):

    menu = {'parent': 'help'}            	         
    return render(request, 'qanda.html', {
                  'menu': menu,
    })


def ask_question(request):

    menu = {'parent': 'help'}            	
    return render(request, 'ask_question.html', {
                  'menu': menu,
                  })
