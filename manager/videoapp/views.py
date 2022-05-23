from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from main.models import TblVideo
# Create your views here.


def updateVideo(request, id):

    video = TblVideo.objects.get(vid_id=id)

    context = {'video': video}

    return render(request, 'videoapp/updateVideo.html', context)


