from django.shortcuts import render
from .models import TblCategory
import base64
# Create your views here.
def category(request):
    categories = TblCategory.objects.all()
    for category in categories:
        category.cat_name = base64.b64decode(category.cat_name)
        category.cat_name = category.cat_name.decode('ascii')
        category.cat_image = base64.b64decode(category.cat_image)
        category.cat_image = category.cat_image.decode('ascii')
    context = {'categories':categories}
    return render(request, 'category/category.html', context)