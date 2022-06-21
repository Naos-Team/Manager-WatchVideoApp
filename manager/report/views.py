from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
from django.core.paginator import Paginator
from django.contrib import messages
from Constant import SERVER_URL
import json
import requests
import pyrebase

config={
    "apiKey": "AIzaSyBY9DlymbmFWWlE4I2ZXVRuxigNgYUUvjs",
    "authDomain": "watch-video-app-ffbc5.firebaseapp.com",
    "databaseURL": "https://watch-video-app-ffbc5-default-rtdb.firebaseio.com",
    "projectId": "watch-video-app-ffbc5",
    "storageBucket": "watch-video-app-ffbc5.appspot.com",
    "messagingSenderId": "926715980598",
    "appId": "1:926715980598:web:ed1183d1b089adb1cea197",
    "measurementId": "G-NS1574JPLV"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()


def decode_Item_Report(report):
    report['uid']= bs.decode_Str(report['uid'])
    report['report_content'] = bs.decode_Str(report['report_content'])
    return report

def decode_Report(reports):
    for report in reports:
        report = decode_Item_Report(report)
    return reports

def decode_Item_Vid(video):
    video['vid_title'] = bs.decode_Str(video['vid_title'])
    return video

def decode_Vid(videos):
    for video in videos:
        video = decode_Item_Vid( video )
    return videos

@login_required(login_url='/login')
def report_home(request, video_type):
    video_search = request.GET.get('tv_search_video') if request.GET.get('tv_search_video') != None else ''
    postObj = {
        'method_name': 'LOAD_ALL_VID_REPORT',
        'vid_search': bs.encode_Str(video_search),
        'vid_type': video_type,
    }
    data = {
        'data': json.dumps(postObj),
    }
    res = requests.post(SERVER_URL, data=data)
    return_object = json.loads(res.content)

    list_vid = decode_Vid(return_object['list'])

    #Paginator
    p = Paginator(list_vid, 10)
    page = request.GET.get('page') 
    list_vids = p.get_page(page)
    nums = "a" * list_vids.paginator.num_pages

    context = {'list_vids':list_vids, 'video_type':video_type, 'nums':nums}
    return render(request, 'report/home_report.html', context)

@login_required(login_url='/login')
def report_main(request, video_id):
    report_search = request.GET.get('tv_search_report') if request.GET.get('tv_search_report') != None else ''
    postObj = {
        'method_name': 'LOAD_REPORT_BY_VID',
        'vid_id': video_id,
        'report_search': bs.encode_Str(report_search),
    }
    data = {
        'data': json.dumps(postObj),
    }
    res = requests.post(SERVER_URL, data=data)
    return_object = json.loads(res.content)

    reports = decode_Report(return_object['list'])

    Paginator
    p = Paginator(reports, 10)
    page = request.GET.get('page') 
    list_res = p.get_page(page)
    nums = "a" * list_res.paginator.num_pages

    try:
        for l in list_res:
            l['name'] = database.child('Users').child(l['uid']).child("user_name").get().val()
            l['url'] = database.child('Users').child(l['uid']).child("photo_url").get().val()
    except Exception as e:
        print(str(e))

    context = {'video_id':video_id, 'list_res':list_res, 'nums': nums, 'num_reports' : len(list_res) }
    return render(request, 'report/list_report.html', context)

@login_required(login_url='/login')
def detail_report(request, report_id):
    postObj = {
        'method_name': 'LOAD_DETAIL_REPORT',
        'report_id': report_id,
    }
    data = {
        'data': json.dumps(postObj),
    }
    res = requests.post(SERVER_URL, data=data)
    return_object = json.loads(res.content)
    report = decode_Report(return_object['list'])
    report_id_de = report[0]['report_id']
    report_content_de = report[0]['report_content']
    report_status_de = report[0]['report_status']
    vid_de = report[0]['vid_id']
    uid_de = report[0]['uid']

    if request.method=="POST": 
        report_id = request.POST.get('report_id')
        uid = request.POST.get('uid')
        vid = request.POST.get('vid')
        report_content = request.POST.get('report_content')
        report_status = request.POST.get('report_status')
        postObj1 = {
            'method_name': 'UPDATE_REPORT',
            'report_id': report_id,
            'uid': bs.encode_Str(uid),
            'vid_id': vid,
            'report_content': bs.encode_Str(report_content),
            'report_status': report_status, 
        }
        data1 = {
            'data': json.dumps(postObj1),
        }
        res1 = requests.post(SERVER_URL, data=data1)
        return_object1 = json.loads(res.content)
        messages.success(request, "Updated successfully")
        return redirect('/report/'+str(vid)+'/report_main')

    context = { 'report_id':report_id_de, 'uid':uid_de, 'vid':vid_de, 'report_content':report_content_de, 'report_status':report_status_de }

    return render(request, 'report/detail_report.html', context)

@login_required(login_url='/login')
def delete_report(request, report_id):
    if request.method=="POST":
        postObj = {
            'method_name': 'DELETE_REPORT',
            'report_id': report_id,
        }
        data = {
            'data': json.dumps(postObj),
        }
        res = requests.post(SERVER_URL, data=data)
        return_object = json.loads(res.content)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))