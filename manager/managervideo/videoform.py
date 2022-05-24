from django.forms import ModelForm
from main.models import TblVideo

class VideoForm(ModelForm):
    class Meta:
        model = TblVideo
        fields = '__all__'
        # fields = ['name', 'body']