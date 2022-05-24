from unicodedata import unidata_version
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from main.models import TblComment, TblReport, TblVideo
from report.forms import ReportForm
from django.db.models import Q
import base64


def report_home(request, video_type):
    video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    if (video_search=="" and video_type==0):
        comments = TblComment.objects.all()
    elif (video_search==""):
        comments = TblComment.objects.filter(vid__vid_type = video_type)
    else:
        if video_search.isnumeric():
            comments = TblComment.objects.filter(Q(vid__vid_id = video_search) | Q(vid__vid_type = video_type) )
        else:
            if video_search.lower() == 'all':
                comments = TblComment.objects.all()
            else:
                comments = TblComment.objects.filter(Q(vid__vid_title = video_search) | Q(vid__vid_type = video_type) )

    context = {'comments': comments, 'video_type':video_type}
    return render(request, 'comment/home_comment.html', context)
