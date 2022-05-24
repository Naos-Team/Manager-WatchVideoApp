import base64
import json
import requests as rq
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from main.models import TblVideo, TblCategory
# Create your views here.


def updateVideo(request, id):

    video = TblVideo.objects.get(vid_id=id)

    if request.method == 'POST':
        # if request.FILES != None:
        #     a = 2
        # else:

        url = 'http://192.168.0.128/test/'
        files = {'file': request.FILES['myfile']}
        r = rq.post(url, files=files)

        js = json.loads(r.content)

        print(js['msg'])


    date_time = video.vid_time.strftime("%Y-%m-%d")

    categories = TblCategory.objects.filter(cat_type=1)
    
    for cat in categories:
        cat.cat_name = base64.b64decode(cat.cat_name).decode('utf-8');
        cat.cat_image = base64.b64decode(cat.cat_image).decode('utf-8');

    video.vid_title = base64.b64decode(video.vid_title).decode('utf-8');
    video.vid_url = base64.b64decode(video.vid_url).decode('utf-8');
    video.vid_thumbnail = base64.b64decode(video.vid_thumbnail).decode('utf-8');
    video.vid_description = base64.b64decode(video.vid_description).decode('utf-8');

    context = {
        'video': video,
        'date': date_time,
        'categories': categories
    }

    return render(request, 'videoapp/updateVideo.html', context)


def videoPlayer(request):

    url = request.POST.get('url') if request.POST.get('url') != None else ''

    context = {'url': url}
    return render(request, 'videoapp/videoPlayer.html', context)
