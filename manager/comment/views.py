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
        videos = TblVideo.objects.all()
    elif (video_search==""):
        videos = TblVideo.objects.filter(vid_type = video_type)
    else:
        if video_search.isnumeric():
            videos = TblVideo.objects.filter(Q(vid_id = video_search) & Q(vid_type = video_type) )
        else:
            if video_search.lower() == 'all':
                videos = TblVideo.objects.all()
            else:
                videos = TblVideo.objects.filter(Q(vid_title = video_search) & Q(vid_type = video_type) )

    cmt_count =  []
    videos_de = decode_Vid(videos)

    for video in videos:
        cmts = TblComment.objects.filter(vid = video)
        cmt_count.append(len(cmts))

    temp = []
    list_vid = []
    for i in range(0,len(videos_de)):
        temp__ = []
        temp__.append(videos_de[i])
        temp__.append(cmt_count[i])
        temp.append(temp__)

    for x,y in temp:
        temp_ = []
        if y!=0:
            temp_.append(x)
            temp_.append(y)
            list_vid.append(temp_)

    context = {'list_vid': list_vid, 'video_type':video_type}
    return render(request, 'comment/home_comment.html', context)

def comment_main(request, video_id):
    cmt_search = request.GET.get('tv_search_cmt') if request.GET.get('tv_search_cmt') != None else ''
    if (cmt_search==""):
        cmts = TblComment.objects.filter(vid__vid_id = video_id)
    else:
        if cmt_search.isnumeric():
            cmts = TblComment.objects.filter(Q(cmt_id = cmt_search) & Q(vid__vid_id = video_id))
        else:
            if cmt_search.lower() == 'all':
                cmts = TblComment.objects.all()
            else:
                cmt_search_en = bs.encode_Str(cmt_search)
                cmts = TblComment.objects.filter(Q(uid__uid__icontains = cmt_search_en) | Q(cmt_text = cmt_search_en) & Q(vid__vid_id = video_id)) 

    video = get_object_or_404(TblVideo, vid_id = video_id)

    context = {
        'cmts': decode_Cmt(cmts), 
        'video_id' : video_id, 
        'video_cat' : bs.decode_Str(video.cat.cat_name), 
        'video_title' : bs.decode_Str(video.vid_title), 
        'video_view': video.vid_view, 
        'num_cmts': len(cmts),
    }
    return render(request, 'comment/list_comment.html', context)

        

def delete_comment(request, cmt_id):
    comment = get_object_or_404(TblComment, cmt_id=cmt_id)
    if request.method=="POST":
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))