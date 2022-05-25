from django.forms import ModelForm
from main.models import TblSettingWeb

class SettingForm(ModelForm):
    class Meta:
        model = TblSettingWeb
        fields = '__all__'
        # fields = ['name', 'body']