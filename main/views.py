from django.shortcuts import render
from .reporting import SQL, tradeReport
from datetime import datetime

def month3(year, month):
    return [f"{str(year-1)}년 {str(month+12-2)}월" if month-2 <= 0 else f"{str(year)}년 {str(month-2)}월",
            f"{str(year-1)}년 {str(month+12-1)}월" if month-1 <= 0 else f"{str(year)}년 {str(month-1)}월",
            f"{str(year)}년 {str(month)}월"]

def index(request):
    selected = request.GET.get("selected", "매출")
    year = datetime.now().year
    month = datetime.now().month

    #misu
    conn = tradeReport()
    client_misu = conn.client_misu()
    fix_misu = conn.fix_misu()
    rant_misu = conn.rant_misu()

    context = {
        'selected': selected,
        'year': year,
        'month': month3(year, month),

        #misu
        'client_misus': client_misu,
        'fix_misus': fix_misu,
        'rant_misus': rant_misu,
    }
    return render(request, "main/index.html", context)

def report(request):
    context = {

    }
    return render(request, "main/report.html", context)