import os
import datetime
import json
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
        'medical_institution': '初期値', 
        'phone_number': '初期値', 
        'office_hours': '初期値', 
    }
    # json_open = open('medical_institutions.json', 'r')
    # medical_institutions = json.load(json_open)

    medical_institutions = {
    "耳鼻科":{
        "病院名":"〇〇耳鼻科",
        "TEL": "000-1234-5678", 
        "営業時間": {
            "Mon": "10:00~12:00, 15:00~17:00",
            "Tue": "10:00~12:00, 15:00~17:00",
            "Wed": "10:00~12:00, 15:00~17:00",
            "Thu": "10:00~12:00, 15:00~17:00",
            "Fri": "10:00~12:00, 15:00~17:00",
            "Sat": "10:00~12:00, 15:00~17:00",
            "Sun": "休業"
        }
    },
    "整形外科":{
        "病院名":"◯△整形外科",
        "TEL": "000-1234-5678", 
        "営業時間": {
            "Mon": "10:00~12:00, 15:00~17:00",
            "Tue": "10:00~12:00, 15:00~17:00",
            "Wed": "10:00~13:00",
            "Thu": "10:00~12:00, 15:00~17:00",
            "Fri": "10:00~12:00, 15:00~17:00",
            "Sat": "10:00~12:00, 15:00~17:00",
            "Sun": "休業"
        }
    }
    }
    if (request.method == 'POST'):
        year, month, day = list(map(int, request.POST['consultation_day'].split("-")))
        dt = datetime.datetime(year, month, day)

        department_dict = {1: "内科", 2: "内科", 3: "歯科", 4: "整形外科", 5: "耳鼻科"}
        department = department_dict[int(request.POST['condition'])]

        institution = medical_institutions[department]
        my_dict['medical_institution'] = institution["病院名"]
        my_dict['phone_number'] = institution["TEL"]        
        my_dict['office_hours'] = institution["営業時間"][dt.strftime('%a')]
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
