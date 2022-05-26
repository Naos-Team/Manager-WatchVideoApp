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
import main.base64_change as bs
from django.core.paginator import Paginator

def decode_Item_Report(report):
    report.uid.uid = bs.decode_Str(report.uid.uid)
    report.report_content = bs.decode_Str(report.report_content)
    return report

def decode_Report(reports):
    for report in reports:
        report = decode_Item_Report(report)
    return reports

def decode_Item_Vid(video):
    video.vid_title = bs.decode_Str(video.vid_title)
    video.vid_url = bs.decode_Str(video.vid_url)
    video.vid_thumbnail = bs.decode_Str(video.vid_thumbnail)
    video.vid_description = bs.decode_Str(video.vid_description)
    return video

def decode_Vid(videos):
    for video in videos:
        video = decode_Item_Vid( video )
    return videos


def report_home(request, video_type):
    video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    if (video_search=="" and video_type==0):
        videos = TblVideo.objects.all()
    elif (video_search==""):
        videos = TblVideo.objects.filter(vid__vid_type = video_type)
    else:
        if video_search.isnumeric():
            videos = TblVideo.objects.filter(Q(vid__vid_id = video_search) & Q(vid__vid_type = video_type) )
        else:
            if video_search.lower() == 'all':
                videos = TblVideo.objects.all()
            else:
                videos = TblVideo.objects.filter(Q(vid__vid_title = video_search) & Q(vid__vid_type = video_type) )
    
    re_count =  []
    temp = []
    videos_de = decode_Vid(videos)

    for video in videos:
        reports = TblReport.objects.filter(vid = video)
        re_count.append(len(reports))

    list_vid = []
    for i in range(0,len(videos_de)):
        temp__ = []
        temp__.append(videos_de[i])
        temp__.append(re_count[i])
        temp.append(temp__)

    for x,y in temp:
        temp_=[]
        if y!=0:
            temp_.append(x)
            temp_.append(y)
            list_vid.append(temp_)

    #Paginator
    p = Paginator(list_vid, 8)
    page = request.GET.get('page') 
    list_vids = p.get_page(page)
    nums = "a" * list_vids.paginator.num_pages

    context = {'list_vid':list_vid, 'video_type':video_type, 'list_vids':list_vids, 'nums': nums}
    return render(request, 'report/home_report.html', context)


def report_main(request, video_id):
    report_search = request.GET.get('tv_search_report') if request.GET.get('tv_search_report') != None else ''
    if (report_search==""):
        reports = TblReport.objects.filter(vid__vid_id = video_id)
    else:
        if report_search.isnumeric():
            reports = TblReport.objects.filter(Q(report_id = report_search) & Q(vid__vid_id = video_id))
        else:
            if report_search.lower() == 'all':
                reports = TblReport.objects.all()
            else:
                reports = TblReport.objects.filter(Q(uid = report_search) & Q(vid__vid_id = video_id))   
    i = len(reports)
    if i == 1 or i == 0:
        num_reports = str(i) + ' Report Here';
    else:
        num_reports = str(i) + ' Reports Here';

    #Paginator
    p = Paginator(reports, 8)
    page = request.GET.get('page') 
    list_res = p.get_page(page)
    nums = "a" * list_res.paginator.num_pages

    context = {'reports': decode_Report(reports), 'video_id':video_id, 'num_reports':num_reports , 'list_res':list_res, 'nums': nums }
    return render(request, 'report/list_report.html', context)

def detail_report(request, report_id):
    report = get_object_or_404(TblReport, report_id=report_id)
    reportid_de = report.report_id
    uid_de = bs.decode_Str(report.uid.uid)
    vid_de = report.vid.vid_id
    report_content_de =  bs.decode_Str(report.report_content)
    print(report_content_de)
    report_status_de =  report.report_status

    if request.method=="POST":
        report_id = request.POST.get('report_id')
        uid = request.POST.get('uid')
        vid = request.POST.get('vid')
        report_content = request.POST.get('report_content')
        report_status = request.POST.get('report_status')

        uid_en = bs.encode_Str(uid)
        report_content_en = bs.encode_Str(report_content)

        context1 = { 'report_id':report_id, 'uid':uid_en, 'vid':vid, 'report_content':report_content_en, 'report_status':report_status}
        form = ReportForm(context1, instance=report)
        if form.is_valid():
            form.save()
            return redirect('/report/'+str(vid)+'/report_main')

    context = { 'report_id':reportid_de, 'uid':uid_de, 'vid':vid_de, 'report_content':report_content_de, 'report_status':report_status_de }

    return render(request, 'report/detail_report.html', context)

def delete_report(request, report_id):
    report = get_object_or_404(TblReport, report_id=report_id)
    if request.method=="POST":
        report.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    
    # video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    # if (video_search=="" and video_type==0):
    #     videos = TblVideo.objects.all()
    # elif (video_search==""):
    #     videos = TblVideo.objects.filter(vid_type = video_type)
    # else:
    #     if video_search.isnumeric():
    #         videos = TblVideo.objects.filter(Q(vid_id = video_search) | Q(vid_type = video_type) )
    #     else:
    #         if video_search.lower() == 'all':
    #             videos = TblVideo.objects.all()
    #         else:
    #             videos = TblVideo.objects.filter(Q(vid_title = video_search) | Q(vid_type = video_type) )

    # context = {'videos': videos, 'video_type':video_type}
    # return render(request, 'report/home_report.html', context)