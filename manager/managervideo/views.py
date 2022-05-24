from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import main.base64_change as base64_change
import base64
# Create your views here.

def encode_Str(columns):
    return base64.b64encode(columns.encode('ascii')).decode('ascii')
    
def decode_Str(columns):
    return base64.b64decode(columns).decode('ascii')

def decode_Item_cate(category):
    category.cat_name = base64_change.decode_Str(category.cat_name)
    category.cat_image = base64_change.decode_Str(category.cat_image)
    return category

def decode_Cate(categories):
    for category in categories:
        category = decode_Item_cate(category)
    return categories

def managervideo(request , pk):
    context = {'choice':pk}
    return render(request, 'managervideo/managervideo.html', context)