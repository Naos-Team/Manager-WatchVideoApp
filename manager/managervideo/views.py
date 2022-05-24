from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory, TblVideo
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
from .videoform import VideoForm
from datetime import date
import base64
# Create your views here.

def decode_Item_cate(category):
    category.cat_name = bs.decode_Str(category.cat_name)
    category.cat_image = bs.decode_Str(category.cat_image)
    return category

def decode_Cate(categories):
    for category in categories:
        category = decode_Item_cate(category)
    return categories

def decode_Item_Video(video):
    video.vid_title = bs.decode_Str(video.vid_title)
    video.vid_url = bs.decode_Str(video.vid_url)
    video.vid_thumbnail = bs.decode_Str(video.vid_thumbnail)
    video.vid_description = bs.decode_Str(video.vid_description)
    return video

def decode_Video(videos):
    for video in videos:
        video = decode_Item_Video(video)
    return videos

def managervideo(request , pk, cat):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q_encode = bs.encode_Str(q) if request.GET.get('q') != None else ''
    categories = TblCategory.objects.filter(Q(cat_type=pk))
    categories = decode_Cate(categories)
    if cat != 0:
        videos = TblVideo.objects.filter( 
            Q(vid_type=pk) &
            Q(cat__cat_id=cat) &
            (Q(vid_title__icontains=q_encode) |
            Q(vid_description__icontains=q_encode))
        )
    else:
          videos = TblVideo.objects.filter(
            Q(vid_type=pk) & 
            (Q(vid_title__icontains=q_encode) |
            Q(vid_description__icontains=q_encode))
        )
    videos = decode_Video(videos)
    context = {'choice':pk, 'cat':cat, 'categories':categories, 'videos':videos, 'test':q_encode}
    return render(request, 'managervideo/managervideo.html', context)

@login_required(login_url='/login')
def addTv(request, pk, cat):
    if request.method == 'POST':
        video_new = {'cat': TblCategory.objects.get(cat_id=request.POST.get('category_vid')),
        'vid_title': bs.encode_Str(request.POST.get('title')), 'vid_url': bs.encode_Str(request.POST.get('url')), 
        'vid_thumbnail': bs.encode_Str('https://s3.cloud.cmctelecom.vn/tinhte2/2019/07/4731556_Cover.jpg'),
        'vid_description': bs.encode_Str(request.POST.get('description')), 'vid_view': "0", 
        'vid_duration': "0", 'vid_time': request.POST.get('time'), 'vid_avg_rate': "0", 
        'vid_status': request.POST.get('vid_status'), 'vid_type': pk, 'vid_is_premium': "0"}
        form = VideoForm(video_new)
        if form.is_valid():
            form.save()
            return redirect("managervideo:managervideo", pk, request.POST.get('category_vid'))
        else:
            return HttpResponse("Error")
    else:
        categories = TblCategory.objects.filter(Q(cat_type=pk))
        categories = decode_Cate(categories)    
        date_time = date.today().strftime("%Y-%m-%d")
        page = 'add'
        context = {'page': page, 'choice':pk, 'cat':cat, 'date_time':date_time, 'categories':categories}
        return render(request, 'managervideo/tvradiodetail.html', context)

@login_required(login_url='/login')
def editTv(request, pk, cat, id):
    video = TblVideo.objects.get(vid_id = id)
    video = decode_Item_Video(video)
    date_time = video.vid_time.strftime("%Y-%m-%d")
    categories = TblCategory.objects.filter(Q(cat_type=pk))
    categories = decode_Cate(categories)
    if request.method == 'POST':
        video_new = {'vid_id': video.vid_id, 'cat': TblCategory.objects.get(cat_id=request.POST.get('category_vid')),
        'vid_title': bs.encode_Str(request.POST.get('title')), 'vid_url': bs.encode_Str(request.POST.get('url')), 
        'vid_thumbnail': bs.encode_Str('https://kyluc.vn/Userfiles/Upload/images/Download/2016/7/11/5e8a770f146b4ec6aef99fcc2e258edd.jpg'),
        'vid_description': bs.encode_Str(request.POST.get('description')), 
        'vid_view': request.POST.get('views'), 'vid_duration': "0", 'vid_time': request.POST.get('time'),
        'vid_avg_rate': request.POST.get('rate'), 'vid_status': request.POST.get('vid_status'), 'vid_type': pk,
        'vid_is_premium': "0"}
        form = VideoForm(video_new, instance=video)
        if form.is_valid():
            form.save()
            return redirect("managervideo:managervideo", pk, request.POST.get('category_vid'))
        else:
            return HttpResponse("Error")
    else:
        page = 'edit'
        context = {'page': page, 'choice':pk, 'cat':cat, 'video':video, 'categories':categories, 'date_time':date_time}
        return render(request, 'managervideo/tvradiodetail.html', context)

@login_required(login_url='/login')
def disableVideo(request, pk, cat, id):
    video = TblVideo.objects.get(vid_id=id)
    video.vid_status = 0 if video.vid_status == 1 else 1
    context = {'vid_id': video.vid_id, 'cat': video.cat, 'vid_title': video.vid_title, 
    'vid_url': video.vid_url, 'vid_thumbnail': video.vid_thumbnail, 'vid_description':video.vid_description,
    'vid_view': video.vid_view, 'vid_duration': video.vid_duration, 'vid_time': video.vid_time,
    'vid_avg_rate': video.vid_avg_rate, 'vid_status': video.vid_status, 'vid_type': video.vid_type,
    'vid_is_premium': video.vid_is_premium}
    form = VideoForm(context, instance=video)
    if form.is_valid():
        form.save()
    return redirect("managervideo:managervideo", pk, cat)