from audioop import add
from dataclasses import field
from hashlib import new
from django import forms
from main.models import TblReport, TblUsers, TblVideo

class ReportForm(forms.ModelForm):
    class Meta:
        model = TblReport
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super(ReportForm, self).__init__(*args, **kwargs)
    #     userobj = TblUsers.objects.filter(uid=self.instance.uid)
    #     videoobj = TblVideo.objects.filter(vid_id=self.instance.vid.vid_id)
    #     self.fields['uid'].queryset = userobj
    #     self.fields['vid'].queryset = videoobj

    # def clean_status(self, *args, **kwargs):
    #     new_status = self.cleaned_data.get('report_status')
    #     if new_status!=1 and new_status!=0:
    #         raise forms.ValidationError("Status must be 1 or 0")
    #     return new_status

        