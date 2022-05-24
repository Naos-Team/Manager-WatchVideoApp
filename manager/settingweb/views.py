from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory, TblVideo, TblSettingWeb
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
from datetime import date
import base64
# Create your views here.
def settingweb(request):
    settingweb = TblSettingWeb.objects.all()
    return HttpResponse(settingweb[0])