from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory, TblVideo, TblSettingWeb
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
from .stwform import SettingForm
from django.core.paginator import Paginator
# Create your views here.

def decode_Item_Setting(stw):
    stw.ads_key_banner = bs.decode_Str(stw.ads_key_banner)
    stw.ads_key_interstial = bs.decode_Str(stw.ads_key_interstial)
    stw.ads_key_openads = bs.decode_Str(stw.ads_key_openads)
    return stw

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

def settingweb(request, able):
    settingweb = TblSettingWeb.objects.get(id=1)
    settingweb = decode_Item_Setting(settingweb)
    context = {}
    
    context = {'able':able, 'settingweb':settingweb}
    return render(request, 'settingweb/settingweb.html', context)

def choiceTrending(request, type):
    settingweb = TblSettingWeb.objects.get(id=1)
    if request.method == 'POST':
        list_trend = request.POST.getlist('list_trend')
        str_temp = 'RESULT'
        for i in list_trend:
            str_temp = str_temp + ':' + i
        if type == "1":
            settingweb.arr_vid_trend = str_temp
        if type == "2":
            settingweb.arr_tv_trend = str_temp
        if type == "3":
            settingweb.arr_radi_trend = str_temp
        settingweb_new = {
            'ads_key_banner': settingweb.ads_key_banner, 
            'ads_key_interstial': settingweb.ads_key_interstial,
            'ad_display_count': settingweb.ad_display_count,
            'ads_key_openads': settingweb.ads_key_openads, 
            'arr_vid_trend': settingweb.arr_vid_trend,
            'arr_tv_trend': settingweb.arr_tv_trend,
            'arr_radi_trend': settingweb.arr_radi_trend
        }
        form = SettingForm(settingweb_new, instance=settingweb)
        if form.is_valid():
            form.save()
            return redirect('settingweb:setting', "1")
        else:
            return HttpResponse(form)
    else:
        list_trend = []
        if type == "1":
            list_trend = settingweb.arr_vid_trend.split(':')
        if type == "2":
            list_trend = settingweb.arr_tv_trend.split(':')
        if type == "3":
            list_trend = settingweb.arr_radi_trend.split(':')
        videos = TblVideo.objects.filter(Q(vid_type=type))
        videos = decode_Video(videos)
        list_trend.pop(0)
        list_trend = [int(item) for item in list_trend]

        #Paginator
        p = Paginator(videos, 5)
        page = request.GET.get('page') 
        list_vid = p.get_page(page)
        nums = "a" * list_vid.paginator.num_pages

        context = {'type':type, 'videos':list_vid, 'list_trend':list_trend, 'nums': nums}
        return render(request, 'settingweb/choicetrend.html', context)

def updateSTW(request):
    settingweb = TblSettingWeb.objects.get(id=1)
    settingweb = decode_Item_Setting(settingweb)
    if request.method == 'POST':
        settingweb_new = {
            'ads_key_banner': bs.encode_Str(request.POST.get('banner')), 
            'ads_key_interstial':bs.encode_Str(request.POST.get('interstial')),
            'ad_display_count':request.POST.get('count'),
            'ads_key_openads': bs.encode_Str(request.POST.get('openads')), 
            'arr_vid_trend': request.POST.get('vid_trend'),
            'arr_tv_trend':  request.POST.get('tv_trend'),
            'arr_radi_trend':  request.POST.get('radio_trend')
        }
        form = SettingForm(settingweb_new, instance=settingweb)
        if form.is_valid():
            form.save()
            return redirect('settingweb:setting', "0")
        else:
            return HttpResponse(form)
    else:
        return HttpResponse("Error")