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
    return render(request, 'comment/home_comment.html', context)
