import json
import requests as rq
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from main.models import TblCategory
from django.db.models import Q
from .categoryform import CategoryForm
from django.contrib.auth.decorators import login_required
import main.base64_change as bs
import base64
from django.core.paginator import Paginator
# Create your views here.
def decode_Item_cate(category):
    category.cat_name = bs.decode_Str(category.cat_name)
    category.cat_image = bs.decode_Str(category.cat_image)
    return category

def decode_Cate(categories):
    for category in categories:
        category = decode_Item_cate(category)
    return categories

def category(request , pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    categories = TblCategory.objects.filter(
        Q(cat_type=pk)
        )

    categories_de = decode_Cate(categories)
    list_search = []
    for category in categories_de:
            if(q in category.cat_name.lower()):
                list_search.append(category)
    p = Paginator(list_search, 8)
    page = request.GET.get('page') 
    list_cats = p.get_page(page)
    nums = "a" * list_cats.paginator.num_pages
    context = {'list_cats':list_cats, 'nums': nums, 'choice':pk}
    return render(request, 'category/category.html', context)

@login_required(login_url='/login')
def addCategory(request, pk):
    if request.method == 'POST':

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

        category_new = {'cat_name':bs.encode_Str(request.POST.get('Name')), 
        'cat_image':thumbnail,
        'cat_type':pk, 'cat_status':request.POST.get('status')}
        form = CategoryForm(category_new)
        if form.is_valid():
            form.save()
            return redirect('category:category', pk = pk)
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

        thumbnail = bs.encode_Str(request.POST.get('thumbnail'))

        #check user update image
        if 'file_img' in request.FILES:
            print("update imageeeeeeeeeeeeeeeeeee")

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
                return redirect('category:category', pk = pk)

        category_new = {'cat_id':category.cat_id,
        'cat_name':bs.encode_Str(request.POST.get('Name')), 
        'cat_image': thumbnail,
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