from unicodedata import unidata_version
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from main.models import TblReport, TblVideo
from report.forms import ReportForm
from django.db.models import Q
import base64


def report_home(request, video_type):
    video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    if (video_search=="" and video_type==0):
        videos = TblVideo.objects.all()
    elif (video_search==""):
        videos = TblVideo.objects.filter(vid_type = video_type)
    else:
        if video_search.isnumeric():
            videos = TblVideo.objects.filter(Q(vid_id = video_search) | Q(vid_type = video_type) )
        else:
            if video_search.lower() == 'all':
                videos = TblVideo.objects.all()
            else:
                videos = TblVideo.objects.filter(Q(vid_title = video_search) | Q(vid_type = video_type) )

    context = {'videos': videos, 'video_type':video_type}
    return render(request, 'report/home_report.html', context)


def report_main(request, video_id):
    report_search = request.GET.get('tv_search_report') if request.GET.get('tv_search_report') != None else ''
    if (report_search==""):
        reports = TblReport.objects.filter(vid__vid_id = video_id)
    else:
        if report_search.isnumeric():
            reports = TblReport.objects.filter(Q(report_id = report_search))
        else:
            if report_search.lower() == 'all':
                reports = TblReport.objects.all()
            else:
                reports = TblReport.objects.filter(Q(uid = report_search))   

    context = {'reports': reports, 'video_id':video_id}
    return render(request, 'report/list_report.html', context)

def detail_report(request, report_id):
    report = get_object_or_404(TblReport, report_id=report_id)
    reportid_de = report.report_id
    uid_d = report.uid.uid
    uid_de = base64.b64decode(uid_d.encode('utf-8')).decode('utf-8')
    vid_de = report.vid.vid_id
    content_d = report.report_content
    report_content_de =  base64.b64decode(content_d).decode('utf-8')
    print(report_content_de)
    report_status_de =  report.report_status

    if request.method=="POST":
        report_id = request.POST.get('report_id')
        uid = request.POST.get('uid')
        vid = request.POST.get('vid')
        report_content = request.POST.get('report_content')
        report_status = request.POST.get('report_status')

        uid_en = base64.b64encode(uid.encode('utf-8')).decode('utf-8')
        report_content_en = base64.b64encode(report_content.encode('utf-8')).decode('utf-8')

        context1 = { 'report_id':report_id, 'uid':uid_en, 'vid':vid, 'report_content':report_content_en, 'report_status':report_status}
        form = ReportForm(context1, instance=report)
        if form.is_valid():
            form.save()
            return redirect('report/')


    context = { 'report_id':reportid_de, 'uid':uid_de, 'vid':vid_de, 'report_content':report_content_de, 'report_status':report_status_de }
  
    
    return render(request, 'report/detail_report.html', context)

def delete_report(request, report_id):
    report = get_object_or_404(TblReport, report_id=report_id)
    if request.method=="POST":
        report.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
