import base64
import json
from ntpath import join
import cv2
import requests as rq
from datetime import date, datetime
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from main.models import TblVideo, TblCategory
from .forms import VideoForm
import re

url_regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def updateVideo(request, id):

    video = TblVideo.objects.get(vid_id=id)
    
    if request.method == 'POST':

        if(request.POST.get('views') == ""):
            messages.error(request, "Views is empty!")
            return redirect('videoapp:update', id=id)

        if(int(request.POST.get('views')) < 0):
            messages.error(request, "Views can not be negative!")
            return redirect('videoapp:update', id=id)

        if(request.POST.get('url') == ""):
            messages.error(request, "URL is empty!")
            return redirect('videoapp:update', id=id)

        #get value form input form
        vid_id = request.POST.get('id')
        cat_id = request.POST.get('cat_id')
        title = base64.b64encode(request.POST.get('title').encode('utf-8')).decode('utf-8')
        vid_url = base64.b64encode(request.POST.get('url').encode('utf-8')).decode('utf-8')
        thumbnail = base64.b64encode(request.POST.get('thumbnail').encode('utf-8')).decode('utf-8')
        description = base64.b64encode(request.POST.get('description').encode('utf-8')).decode('utf-8')
        views = request.POST.get('views')
        time = request.POST.get('time')
        cat_id = request.POST.get('cat_id')
        rate = request.POST.get('rate')
        status = request.POST.get('status')

        data = cv2.VideoCapture(request.POST.get('url'))
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(data.get(cv2.CAP_PROP_FPS))
        seconds = int(frames / fps)

        #check user update image
        if 'file_img' in request.FILES:
            print("update image")

            url = 'http://localhost/watchvideoapp/uploadImage.php'
            files = {'file': request.FILES['file_img']}
            data = {'crr': request.POST.get('thumbnail')}
            res = rq.post(url, files=files, params=data)
        
            js = json.loads(res.content)
            if(js['status'] == 1):
                image_dir = 'http://localhost/watchvideoapp/image/'+js['dir'];
                thumbnail = base64.b64encode(image_dir.encode('utf-8')).decode('utf-8')
            else:
                messages.error(request, "Something wrong when upload image, please try again!")
                return redirect('videoapp:update', id=id)

        #save to form
        updated_video = {
            'vid_id': vid_id,
            'cat': TblCategory.objects.get(cat_id=cat_id),
            'vid_title': title,
            'vid_url': vid_url,
            'vid_thumbnail': thumbnail,
            'vid_description': description,
            'vid_view': views,
            'vid_duration': seconds,
            'vid_time': datetime.strptime(time, '%Y-%m-%d'),
            'vid_avg_rate': rate,
            'vid_status': status,
            'vid_type': 1,
            'vid_is_premium': 0
        }
    
        form = VideoForm(updated_video, instance = video)

        if form.is_valid():
            form.save()
            messages.success(request, "This video is updated!")
        else:

            for err in form.errors.items():

                if(err[0] == 'vid_title'):
                    messages.error(request, 'Title: ' + err[1][0])
                elif(err[0] == 'vid_description'):
                    messages.error(request, 'Description: ' + err[1][0])
                elif(err[0] == 'vid_view'):
                    messages.error(request, 'Views: ' + err[1][0])
                elif(err[0] == 'vid_url'):
                    messages.error(request, 'URL: ' + err[1][0])
                else:
                    messages.error(request, 'Form is invalid')
                

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
        'mode': 'update',
        'video': video,
        'date': date_time,
        'categories': categories
    }

    return render(request, 'videoapp/updateVideo.html', context)


def createVideo(request):
    
    if request.method == 'POST':
    
        if(request.POST.get('views') == ""):
            messages.error(request, "Views is empty!")
            return redirect('videoapp:create')    

        if(int(request.POST.get('views')) < 0):
            messages.error(request, "Views can not be negative!")
            return redirect('videoapp:create')

        if(request.POST.get('url') == ""):
            messages.error(request, "URL is empty!")
            return redirect('videoapp:create')

        if(re.match(url_regex, request.POST.get('url')) is None):
            messages.error(request, "Please enter a correct URL!")
            return redirect('videoapp:create')

        #get value form input form
        vid_id = request.POST.get('id')
        cat_id = request.POST.get('cat_id')
        title = base64.b64encode(request.POST.get('title').encode('utf-8')).decode('utf-8')
        vid_url = base64.b64encode(request.POST.get('url').encode('utf-8')).decode('utf-8')
        thumbnail = base64.b64encode(request.POST.get('thumbnail').encode('utf-8')).decode('utf-8')
        description = base64.b64encode(request.POST.get('description').encode('utf-8')).decode('utf-8')
        views = request.POST.get('views')
        time = request.POST.get('time')
        cat_id = request.POST.get('cat_id')
        rate = request.POST.get('rate')
        status = request.POST.get('status')

        data = cv2.VideoCapture(request.POST.get('url'))
        frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
        fps = int(data.get(cv2.CAP_PROP_FPS))
        seconds = int(frames / fps)

        #check user update image
        if 'file_img' in request.FILES:
            print("update image")

            url = 'http://localhost/watchvideoapp/uploadImage.php'
            files = {'file': request.FILES['file_img']}
            data = {'crr': request.POST.get('thumbnail')}
            res = rq.post(url, files=files, params=data)
        
            js = json.loads(res.content)
            if(js['status'] == 1):
                image_dir = 'http://localhost/watchvideoapp/image/'+js['dir'];
                thumbnail = base64.b64encode(image_dir.encode('utf-8')).decode('utf-8')
            else:
                messages.error(request, "Something wrong when upload image, please try again!")
                return redirect('videoapp:create')
        else:
            messages.error(request, "Thumbnail is required!")
            return redirect('videoapp:create')

        #save to form
        updated_video = {
            'vid_id': vid_id,
            'cat': TblCategory.objects.get(cat_id=cat_id),
            'vid_title': title,
            'vid_url': vid_url,
            'vid_thumbnail': thumbnail,
            'vid_description': description,
            'vid_view': views,
            'vid_duration': seconds,
            'vid_time': datetime.strptime(time, '%Y-%m-%d'),
            'vid_avg_rate': 0,
            'vid_status': status,
            'vid_type': 1,
            'vid_is_premium': 0
        }
    
        form = VideoForm(updated_video)

        if form.is_valid():
            video = form.save()
            messages.success(request, "Create successfully!")
            return redirect('videoapp:update', video.vid_id)
            
        else:

            for err in form.errors.items():

                if(err[0] == 'vid_title'):
                    messages.error(request, 'Title: ' + err[1][0])
                elif(err[0] == 'vid_description'):
                    messages.error(request, 'Description: ' + err[1][0])
                elif(err[0] == 'vid_view'):
                    messages.error(request, 'Views: ' + err[1][0])
                elif(err[0] == 'vid_url'):
                    messages.error(request, 'URL: ' + err[1][0])
                else:
                    messages.error(request, 'Form is invalid')
                

        return redirect('videoapp:create')

    categories = TblCategory.objects.filter(cat_type=1)

    for cat in categories:
        cat.cat_name = base64.b64decode(cat.cat_name).decode('utf-8')
        cat.cat_image = base64.b64decode(cat.cat_image).decode('utf-8')

    now = datetime.now()
    date_time = now.strftime('%Y-%m-%d')
    
    default_video = {
            'vid_title': 'New video title',
            'vid_url': 'New video url',
            'vid_thumbnail': 'https://socialistmodernism.com/wp-content/uploads/2017/07/placeholder-image.png?w=640',
            'vid_description': 'New video description',
            'vid_view': 0,
            'vid_status': 1,
        }

    context = {
        'mode': 'create',
        'date': date_time,
        'video': default_video,
        'categories': categories
    }

    return render(request, 'videoapp/updateVideo.html', context)


def videoPlayer(request):

    url = request.POST.get('url') if request.POST.get('url') != None else ''

    context = {'url': url}
    return render(request, 'videoapp/videoPlayer.html', context)
