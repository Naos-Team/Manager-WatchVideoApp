import base64
import json
import requests as rq
from datetime import datetime
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from main.models import TblVideo, TblCategory
from .forms import VideoForm
# Create your views here.


def updateVideo(request, id):

    video = TblVideo.objects.get(vid_id=id)

    if request.method == 'POST':

        vid_id = request.POST.get('id')
        cat_id = request.POST.get('cat_id')
        title = base64.b64encode(request.POST.get('title').encode('utf-8')).decode('utf-8')
        url = base64.b64encode(request.POST.get('url').encode('utf-8')).decode('utf-8')
        thumbnail = base64.b64encode(request.POST.get('thumbnail').encode('utf-8')).decode('utf-8')
        description = base64.b64encode(request.POST.get('description').encode('utf-8')).decode('utf-8')
        views = request.POST.get('views')
        time = request.POST.get('time')
        cat_id = request.POST.get('cat_id')

        # updated_video.vid_title = title
        # updated_video.vid_url = url
        # updated_video.vid_thumbnail = thumbnail
        # updated_video.vid_description = description
        # updated_video.vid_view = views
        # updated_video.cat = TblCategory.objects.get(cat_id=cat_id)
        # updated_video.vid_time = datetime.strptime(time, '%Y-%m-%d')

        updated_video = {
            'vid_id': '',
            'cat': 2,
            'vid_title': 2,
            'vid_url': 2,
            'vid_thumbnail': 2,
            'vid_description': 2,
            'vid_view': 2,
            'vid_duration': 2,
            'vid_time': 2,
            'vid_avg_rate': 2,
            'vid_status': 2,
            'vid_type': 2,
            'vid_is_premium': 0
        }

        if 'file_img' in request.FILES:
            print("update image")

            url = 'http://localhost/watchvideoapp/uploadImage.php'
            files = {'file': request.FILES['file_imsg']}
            res = rq.post(url, files=files)
            js = json.loads(res.content)

            if(js['status'] == 1):
                thumbnail = 'http://localhost/watchvideoapp/image/'+js['dir'];
                updated_video.vid_thumbnail = base64.b64encode(thumbnail.encode('utf-8')).decode('utf-8')
            else:
                messages.error(request, "Something wrong when upload image, please try again!")
                return redirect('videoapp:update', id=id)
    
        form = VideoForm(updated_video)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Form is invalid!")
        return redirect('videoapp:update', id=id)
            
    date_time = video.vid_time.strftime("%Y-%m-%d")

    categories = TblCategory.objects.filter(cat_type=1)

    for cat in categories:
        cat.cat_name = base64.b64decode(cat.cat_name).decode('utf-8')
        cat.cat_image = base64.b64decode(cat.cat_image).decode('utf-8')

    video.vid_title = base64.b64decode(video.vid_title).decode('utf-8')
    video.vid_url = base64.b64decode(video.vid_url).decode('utf-8')
    video.vid_thumbnail = base64.b64decode(video.vid_thumbnail).decode('utf-8')
    video.vid_description = base64.b64decode(video.vid_description).decode('utf-8')

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
