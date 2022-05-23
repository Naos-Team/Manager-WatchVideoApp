from django.forms import ModelForm
from main.models import TblCategory

class CategoryForm(ModelForm):
    class Meta:
        model = TblCategory
        fields = '__all__'
        # fields = ['name', 'body']