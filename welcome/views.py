import os
import datetime
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView
from .forms import TestForm, PracticeForm

# Create your views here.
def practice(request):

    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)
    
    my_dict = {
        'form': PracticeForm(),
        'insert_forms': '初期値', 
    }

    if (request.method == 'POST'):
        year, month, day = list(map(int, request.POST['consultation_day'].split("-")))
        dt = datetime.datetime(year, month, day)
        
        my_dict['insert_forms'] = '文字列:' + dt.strftime('%a') + '\n整数型:' + request.POST['condition']
        my_dict['form'] = PracticeForm(request.POST)

    return render(request, 'welcome/practice.html', my_dict)


def input_test(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)
    my_dict = {
        'insert_something': '表示テスト',
        'form': TestForm(),
        'insert_forms': '初期値', 
    }

    if (request.method == 'POST'):
        my_dict['insert_forms'] = '文字列:' + request.POST['text'] + '\n整数型:' + request.POST['num']
        my_dict['form'] = TestForm(request.POST)

    return render(request, 'welcome/input_test.html', my_dict)


def index(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def index_ja(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index_ja.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())
