from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from dateutil.parser import parse
from main.models import TblVideo, TblCategory
# Create your views here.


def updateVideo(request, id):

    video = TblVideo.objects.get(vid_id=id)

    date_time = video.vid_time.strftime("%Y-%m-%d")

    categories = TblCategory.objects.filter(cat_type=1)

    context = {
        'video': video, 
        'date': date_time,
        'categories': categories
    }

    return render(request, 'videoapp/updateVideo.html', context)


