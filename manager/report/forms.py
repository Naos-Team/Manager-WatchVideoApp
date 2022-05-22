from audioop import add
from dataclasses import field
from hashlib import new
from django import forms
from main.models import TblReport, TblUsers, TblVideo

class ReportForm(forms.ModelForm):
    report_id = forms.IntegerField()
    uid = forms.CharField()
    vid = forms.IntegerField()
    report_content = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder':'Report Content'
            }
        )
    )
    report_status = forms.IntegerField(
         initial='1',
         widget=forms.TextInput(
            attrs={
                'class': 'form-control', 
                'placeholder':'Report Status',

            }
        )
    )
    class Meta:
        model = TblReport
        fields = ['report_id', 'uid', 'vid', 'report_content', 'report_status']
