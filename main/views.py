from django.shortcuts import render
from .reporting import SQL, tradeReport
# Create your views here.


def index(request):

    context = {

    }
    return render(request, "main/index.html")

def report(request):
    conn = tradeReport()
    client_misu = conn.client_misu()
    fix_misu = conn.fix_misu()
    rant_misu = conn.rant_misu()
    context = {
        'client_misus': client_misu,
        'fix_misus': fix_misu,

    }
    return render(request, "main/report.html", context)