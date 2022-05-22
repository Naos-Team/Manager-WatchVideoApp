from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from main.models import TblReport
from report.forms import ReportForm


def report_main(request):
    reports = TblReport.objects.all()
    context = {'reports': reports}
    return render(request, 'report/list_report.html', context)

def detail_report(request, report_id):
    report = get_object_or_404(TblReport, report_id=report_id)
    context = {'report': report}
    return render(request, 'report/detail_report.html', context)
