from unicodedata import unidata_version
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from main.models import TblComment, TblReport, TblVideo, TblCategory
from report.forms import ReportForm
from django.db.models import Q
import base64
import main.base64_change as bs

def decode_Item_Cmt(comment):
    comment.uid.uid = bs.decode_Str(comment.uid.uid)
    comment.cmt_text = bs.decode_Str(comment.cmt_text)
    return comment

def decode_Cmt(comments):
    for comment in comments:
        comment = decode_Item_Cmt(comment)
    return comments



def comment_home(request, video_type):
    # video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    # if (video_search=="" and video_type==0):
    #     comments = TblVideo.objects.all()
    # elif (video_search==""):
    #     comments = TblVideo.objects.filter(vid__vid_type = video_type)
    # else:
    #     if video_search.isnumeric():
    #         comments = TblVideo.objects.filter(Q(vid__vid_id = video_search) | Q(vid__vid_type = video_type) )
    #     else:
    #         if video_search.lower() == 'all':
    #             comments = TblVideo.objects.all()
    #         else:
    #             comments = TblVideo.objects.filter(Q(vid__vid_title = video_search) | Q(vid__vid_type = video_type) )

    # context = {'comments': comments, 'video_type':video_type}
    # return render(request, 'comment/home_comment.html', context)

    video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    if (video_search=="" and video_type==0):
        comments = TblVideo.objects.all()
    elif (video_search==""):
        comments = TblVideo.objects.filter(vid_type = video_type)
    else:
        if video_search.isnumeric():
            comments = TblVideo.objects.filter(Q(vid_id = video_search) | Q(vid_type = video_type) )
        else:
            if video_search.lower() == 'all':
                comments = TblVideo.objects.all()
            else:
                comments = TblVideo.objects.filter(Q(vid_title = video_search) | Q(vid_type = video_type) )

    context = {'comments': comments, 'video_type':video_type}
    return render(request, 'comment/home_comment.html', context)

def comment_main(request, video_id):
    cmt_search = request.GET.get('tv_search_cmt') if request.GET.get('tv_search_cmt') != None else ''
    if (cmt_search==""):
        cmts = TblComment.objects.filter(vid__vid_id = video_id)
    else:
        if cmt_search.isnumeric():
            cmts = TblComment.objects.filter(Q(report_id = cmt_search) | Q(vid__vid_id = video_id))
        else:
            if cmt_search.lower() == 'all':
                cmts = TblComment.objects.all()
            else:
                cmts = TblComment.objects.filter(Q(uid = cmt_search) | Q(vid__vid_id = video_id)) 

    video = get_object_or_404(TblVideo, vid_id = video_id)

    video_view = video.vid_view

    context = {
        'cmts': decode_Cmt(cmts), 
        'video_id' : video_id, 
        'video_cat' : bs.decode_Str(video.cat.cat_name), 
  
        'video_view': video_view, 
        'num_cmts': len(cmts),
    }
    return render(request, 'comment/list_comment.html', context)

        #   'video_title' : bs.decode_Str(video.vid_title), 

def delete_comment(request, cmt_id):
    comment = get_object_or_404(TblComment, cmt_id=cmt_id)
    if request.method=="POST":
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))