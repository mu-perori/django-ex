import os
import datetime
import json
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import database, backend_api
from .models import PageView
from .forms import PracticeForm

module_dir = os.path.dirname(__file__)
json_path = os.path.join(module_dir, 'medical_institutions.json')

# Create your views here.
def index(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'welcome/index.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })


def test(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)
    
    return_dict = {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count(),
        'form': PracticeForm(),
        'medical_institution': '　', 
        'phone_number': '　', 
        'office_hours': '　', 
    }

    medical_institutions = read_medical_institutions()

    if (request.method == 'POST'):
        year, month, day = list(map(int, request.POST['consultation_day'].split("-")))
        dt = datetime.datetime(year, month, day)

        department_dict = {1: "内科", 2: "内科", 3: "歯科", 4: "整形外科", 5: "耳鼻科", 6: "皮膚科", 7: "整形外科"}
        department = department_dict[int(request.POST['condition'])]

        institution = medical_institutions[department]
        return_dict['medical_institution'] = institution["病院名"]
        return_dict['phone_number'] = institution["TEL"]        
        return_dict['office_hours'] = institution["営業時間"][dt.strftime('%a')]
        return_dict['form'] = PracticeForm(request.POST)

    return render(request, 'test/site/public/index.html', return_dict)

def measurements(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'test/site/public/measurements.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

# htmlとhtmlに表示するデータとで分ける
# measurementController.jsの9行目も変更
def measurementsdata(request):
    measurements = {
        "smokerstatus": "Former smoker",
        "dia": 88,
        "sys": 130,
        "bmi": 19.74,
        "bmirange": "normal",
        "weight": 54.42,
        "height": 1.6603
    }
    return HttpResponse(json.dumps(measurements))

def jee(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'test/site/public/jee.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def setting(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'test/site/public/setting.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def about(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'test/site/public/about.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def admin(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'test/site/public/admin.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def labs(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    return render(request, 'test/site/public/labs.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

# CSRF検証を無効化したい関数にのみアノテーション追加(これがないと403エラーになる)
@csrf_exempt
def login(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)

    if (request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        patient_login = backend_api.patient_login("", username, password)

    return render(request, 'test/site/public/login.html', {
        'hostname': hostname,
        'database': database.info(),
        'count': PageView.objects.count()
    })

def read_medical_institutions():
    json_open = open(json_path, 'r')
    medical_institutions = json.load(json_open)
    return medical_institutions

# app.jsより移植
MODE = {
    "TEST": 1,
    "Z": 2,
    "OPENSHIFT": 3
}
CURRENTMODE = MODE['TEST']
API_URL = ""

def mode(request):
    global CURRENTMODE
    # app.jsの30-38行目を移植
    if (request.method == 'POST'):
        if 'mode' in request.GET:
            CURRENTMODE = request.GET['mode']
        if 'url' in request.GET:
            CURRENTMODE = request.GET['url']
    
        return HttpResponse({
            "modes": MODE,
            "mode": CURRENTMODE
        })
    # app.jsの40-44行目を移植
    elif (request.method == 'GET'):
        return HttpResponse({
            "modes": MODE,
            "mode": CURRENTMODE
        })
    else:
        return

def info(request):
    global CURRENTMODE

    if (request.method == 'GET'):

        # ここはbackend_api.pyの関数を呼ぶように変更が必要。
        if (CURRENTMODE == MODE['TEST']):
            # patientdata = {
            #     "personal": {
            #         "name": "Ralph DAlmeida",
            #         "age": 38,
            #         "gender": "male",
            #         "street": "34 Main Street",
            #         "city": "Toronto",
            #         "zipcode": "M5H 1T1"
            #     },
            #     "medications": ["Metoprolol", "ACE inhibitors", "Vitamin D"],
            #     "appointments": ["2018-01-15 1:00 - Dentist", "2018-02-14 4:00 - Internal Medicine", "2018-09-30 8:00 - Pediatry"]
            # }

            patientinfo = backend_api.get_patient_info("", request.GET.get('id'))
            patientdata = {
                "personal": patientinfo,
                "medications": ["Metoprolol", "ACE inhibitors", "Vitamin D"],
                "appointments": ["2018-01-15 1:00 - Dentist", "2018-02-14 4:00 - Internal Medicine", "2018-09-30 8:00 - Pediatry"]
            }

            return HttpResponse(json.dumps(patientdata))
            # return HttpResponse(patientdata) これだと動かない
            # REST APIではjson.dumpsが必要
        else:
            return
