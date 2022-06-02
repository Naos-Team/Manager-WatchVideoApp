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
from django.core.paginator import Paginator
from Constant import SERVER_URL
import json
import requests

def decode_Item_Cmt(comment):
    comment.uid.uid = bs.decode_Str(comment.uid.uid)
    comment.cmt_text = bs.decode_Str(comment.cmt_text)
    return comment

def decode_Cmt(comments):
    for comment in comments:
        comment = decode_Item_Cmt(comment)
    return comments

def decode_Item_Vid(video):
    video.vid_title = bs.decode_Str(video.vid_title)
    video.vid_url = bs.decode_Str(video.vid_url)
    video.vid_thumbnail = bs.decode_Str(video.vid_thumbnail)
    video.vid_description = bs.decode_Str(video.vid_description)
    return video

def decode_Vid(videos):
    for video in videos:
        video = decode_Item_Vid(video)
    return videos




def comment_home(request, video_type):
    video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    postObj = {
        'method_name': 'LOAD_ALL_VID_CMT',
        'vid_search': video_search,
        'vid_type': video_type,
    }
    data = {
        'data': json.dumps(postObj),
    }
    res = requests.post(SERVER_URL, data=data)
    return_object = json.loads(res.content)

    list_vid = return_object['list']

    # #Paginator
    # p = Paginator(list_vid, 8)
    # page = request.GET.get('page') 
    # list_vids = p.get_page(page)
    # nums = "a" * list_vids.paginator.num_pages

    # context = {'list_vid': list_vid, 'video_type':video_type,}
    return render(request, 'comment/home_comment.html', context)

@login_required(login_url='/login')
def comment_main(request, video_id):
    cmt_search = request.GET.get('tv_search_cmt') if request.GET.get('tv_search_cmt') != None else ''
    postObj = {
        'method_name': 'LOAD_CMT_BY_VID_SEARCH',
        'vid_id': video_id,
        'cmt_search': cmt_search,
    }
    data = {
        'data': json.dumps(postObj),
    }
    res = requests.post(SERVER_URL, data=data)
    return_object = json.loads(res.content)

    reports = return_object['list']

    context = {
        # 'cmts': cmts_de, 
        # 'video_id' : video_id, 
        # 'video_cat' : bs.decode_Str(video.cat.cat_name), 
        # 'video_title' : bs.decode_Str(video.vid_title), 
        # 'video_view': video.vid_view, 
        # 'num_cmts': len(cmts),
        # 'nums': nums,
        # 'list_cmts': list_cmts,
    }
    return render(request, 'comment/list_comment.html', context)

        

def delete_comment(request, cmt_id):
    comment = get_object_or_404(TblComment, cmt_id=cmt_id)
    if request.method=="POST":
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))