import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from . import database
from .models import PageView

# Create your views here.
def input_test(request):
    """Takes an request object as a parameter and creates an pageview object then responds by rendering the index view."""
    hostname = os.getenv('HOSTNAME', 'unknown')
    PageView.objects.create(hostname=hostname)
    
    return render(request, 'welcome/input_test.html')

def get_nyuuryoku(request):
    message = 'データ受け取ったよ！'
    if request.method == 'POST':
        nyuryoku1 = request.POST['nyuryoku1']
        nyuryoku2 = request.POST['nyuryoku2']
        nyuryoku3 = request.POST['nyuryoku3']
        
        params = {
            "nyuryoku1": nyuryoku1,
            "nyuryoku2": nyuryoku2,
            "nyuryoku3": nyuryoku3,
            "message": message,
        }

        return render(request, 'welcome/input_test.html', params)


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
