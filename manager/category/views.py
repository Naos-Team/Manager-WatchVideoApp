from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory
from django.db.models import Q
from .categoryform import CategoryForm
from django.contrib.auth.decorators import login_required
import base64
# Create your views here.

def encode_Str(columns):
    return base64.b64encode(columns.encode('ascii')).decode('ascii')    

def decode_Item_cate(category):
    category.cat_name = base64.b64decode(category.cat_name)
    category.cat_name = category.cat_name.decode('ascii')
    category.cat_image = base64.b64decode(category.cat_image)
    category.cat_image = category.cat_image.decode('ascii')
    return category

def decode_Cate(categories):
    for category in categories:
        category = decode_Item_cate(category)
    return categories

def category(request , pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    q_encode = encode_Str(q) if request.GET.get('q') != None else ''
    categories = TblCategory.objects.filter(
        Q(cat_type=pk) &
        Q(cat_name__icontains= q_encode) |
        Q(cat_id__icontains= q)
        )
    context = {'categories':decode_Cate(categories), 'choice':pk}
    return render(request, 'category/category.html', context)

@login_required(login_url='/login')
def addCategory(request, pk):
    if request.method == 'POST':
        category_new = {'cat_name':encode_Str(request.POST.get('Name')), 
        'cat_image':encode_Str('https://vcdn1-dulich.vnecdn.net/2020/11/21/1-1605972569.jpg?w=1200&h=0&q=100&dpr=1&fit=crop&s=Gs5VBQ9eOvNSi6tNWUhkRQ'),
        'cat_type':pk, 'cat_status':request.POST.get('status')}
        form = CategoryForm(category_new)
        if form.is_valid():
            form.save()
            return redirect('category:category', pk)
        else:
            return HttpResponse("Error")
    else:
        page = 'add'
        context = {'page': page, 'choice':pk}
        return render(request, 'category/categorydetail.html', context)

@login_required(login_url='/login')
def editCategory(request, pk, id):
    category = TblCategory.objects.get(cat_id = id)
    category = decode_Item_cate(category)
    if request.method == 'POST':
        category_new = {'cat_id':category.cat_id,
        'cat_name':encode_Str(request.POST.get('Name')), 
        'cat_image':encode_Str('https://media.bongda.com.vn/resize/800x800/files/news/2019/06/23/torres-tiet-lo-ly-do-giai-nghe-chi-ra-cau-thu-hay-nhat-tung-choi-cung-152947.jpg'),
        'cat_type':category.cat_type, 'cat_status':request.POST.get('status')}
        form = CategoryForm(category_new, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category:category', pk)
        else:
            return HttpResponse("Error")
    else:
        page = 'edit'
        context = {'page': page, 'choice':pk, 'category':category}
        return render(request, 'category/categorydetail.html', context)

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