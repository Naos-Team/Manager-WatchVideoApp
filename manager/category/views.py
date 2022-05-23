from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory
from django.db.models import Q
from .categoryform import CategoryForm
from django.contrib.auth.decorators import login_required
import base64
# Create your views here.

def decode_Cate(categories):
    for category in categories:
        category.cat_name = base64.b64decode(category.cat_name)
        category.cat_name = category.cat_name.decode('ascii')
        category.cat_image = base64.b64decode(category.cat_image)
        category.cat_image = category.cat_image.decode('ascii')
    return categories

def category(request , pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q_encode = base64.b64encode(q.encode('ascii')).decode('ascii') if request.GET.get('q') != None else ''
    categories = TblCategory.objects.filter(
        Q(cat_type=pk) &
        Q(cat_name__icontains= q_encode)
        )
    context = {'categories':decode_Cate(categories), 'choice':pk}
    return render(request, 'category/category.html', context)

@login_required(login_url='/login')
def disableCategory(request, pk, id):
    category = TblCategory.objects.get(cat_id = id)
    category.cat_status = 0 if category.cat_status == 1 else 1
    context = {'cat_id':category.cat_id, 'cat_name':category.cat_name, 
        'cat_image': category.cat_image, 'cat_type':category.cat_type, 'cat_status':category.cat_status}
    form = CategoryForm(context, instance=category)
    if form.is_valid():
        form.save()
    return redirect("category:category", pk)